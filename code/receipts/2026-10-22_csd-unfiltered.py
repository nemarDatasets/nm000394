"""Value type and power below 1 Hz / above 30 Hz of the stored CSD segments in nm000394.

Usage: python 2026-10-22_csd-unfiltered.py <nm000394 root> <nm000394 git clone>

<nm000394 root> holds the BIDS files read, <nm000394 git clone> gives origin/main (sidecars,
git-annex keys).
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import mne
import numpy as np
import pandas as pd
import scipy
import scipy.signal

REF = "origin/main"
LOW_HZ, HIGH_HZ = 1.0, 30.0


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(1 << 24):
            h.update(chunk)
    return h.hexdigest()


def git(clone: Path, *args: str) -> bytes:
    out = subprocess.run(["git", "-C", clone, *args], capture_output=True)
    assert out.returncode == 0, out.stderr.decode()
    return out.stdout


def same_as_main(root: Path, clone: Path, rel: Path) -> bool:
    """File equals origin/main: sha256 = git-annex key, or bytes = git blob."""
    blob = git(clone, "show", f"{REF}:{rel}")
    if blob.startswith(b"/annex/objects/SHA256E-"):
        return blob.decode().split("--")[1].split(".")[0] == digest(root / rel)
    return blob == (root / rel).read_bytes()


def markdown(table: pd.DataFrame) -> str:
    lines = ["| " + " | ".join(table.columns) + " |", "|---" * table.shape[1] + "|"]
    for row in table.itertuples(index=False):
        cells = (f"{v:.1f}" if isinstance(v, float) else str(v) for v in row)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main(root: Path, clone: Path) -> None:
    print(f"mne {mne.__version__}, numpy {np.__version__}, scipy {scipy.__version__}")
    print(f"{REF} of the clone: {git(clone, 'rev-parse', REF).decode().strip()}")
    runs, channels = [], []
    for vhdr in sorted(root.glob("sub-*/ieeg/*_ieeg.vhdr")):
        rel = vhdr.relative_to(root)
        sidecar = json.loads(git(clone, "show", f"{REF}:{rel.with_suffix('.json')}"))
        raw = mne.io.read_raw_brainvision(vhdr, preload=True, verbose="error")
        # stored float32 values (resolution 1; empty header unit read as µV)
        x = np.float32(raw.get_data(units="uV"))
        f, psd = scipy.signal.periodogram(
            x.astype(np.float64), raw.info["sfreq"], window="boxcar", detrend="constant"
        )
        total = psd.sum(axis=1)
        low = 100 * psd[:, (f > 0) & (f < LOW_HZ)].sum(axis=1) / total
        high = 100 * psd[:, f > HIGH_HZ].sum(axis=1) / total
        name = rel.name.removesuffix("_desc-csd_ieeg.vhdr").removeprefix("sub-01_")
        runs.append(
            {
                "run": name,
                "source CSV": Path(sidecar["SourceFile"]).name,
                "vhdr+eeg == main": all(
                    same_as_main(root, clone, rel.with_suffix(s))
                    for s in (".vhdr", ".eeg")
                ),
                "Hz": f"{raw.info['sfreq']:g}",
                "samples x ch": f"{raw.n_times} x {len(raw.ch_names)}",
                "integers": bool(np.all(x == np.round(x))),
                "min": f"{x.min():.0f}",
                "max": f"{x.max():.0f}",
                "% < 0": 100 * float((x < 0).mean()),
                "distinct values": len(np.unique(x)),
                "% power < 1 Hz (min-max ch)": f"{low.min():.1f}-{low.max():.1f}",
                "% power > 30 Hz (min-max ch)": f"{high.min():.1f}-{high.max():.1f}",
            }
        )
        channels += [
            {"channel": c, "low": lo, "high": hi}
            for c, lo, hi in zip(raw.ch_names, low, high)
        ]
    print("\n" + markdown(pd.DataFrame(runs)))
    ch = pd.DataFrame(channels)
    per_ch = ch.groupby("channel", sort=False).agg(
        n=("low", "size"),
        low_min=("low", "min"),
        low_median=("low", "median"),
        low_max=("low", "max"),
        high_min=("high", "min"),
        high_median=("high", "median"),
        high_max=("high", "max"),
    )
    print("\n" + markdown(per_ch.reset_index()))
    print(
        f"\nall {len(ch)} channel-segments: % power < {LOW_HZ:g} Hz "
        f"{ch.low.min():.1f}-{ch.low.max():.1f} (median {ch.low.median():.1f}); "
        f"% power > {HIGH_HZ:g} Hz median {ch.high.median():.2f} "
        f"(range {ch.high.min():.1f}-{ch.high.max():.1f})"
    )


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
