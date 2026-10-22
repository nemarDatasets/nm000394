# Receipt: README: stored CSD is unfiltered and not rank-normalised

**Claim**: the stored CSD values precede the paper's 1-30 Hz filtering and rank normalisation: they are signed integers (not ranks) with 21-78% of the power below 1 Hz and a median 6.5% above 30 Hz (4 channels x 34 segments).

**PR**: nemarDatasets/nm000394#3; this receipt is one commit on top of head 961f4878.

## Source

- NEMAR nm000394 `origin/main` e8ea3e982d60d4cbbf6c4abf1dc7a67f7ffe42b8: all 34 `sub-01/ieeg/sub-01_task-{seizure,interictal}_run-XX_desc-csd_ieeg.{vhdr,eeg}`. Each `.eeg` sha256 equals its git-annex key and each `.vhdr` equals its git blob (column `vhdr+eeg == main`). Upstream: G-Node GIN zsigmondbenko/intracranial_csd, commit 3e5bd99b6919d3fa33e8c4d8d50c714f131dc20b (`SourceDatasets`); `sub-01_scans.tsv` and each ieeg.json `SourceFile` name the CSV behind each run. The CSVs were not re-read here.
- Benkő et al., arXiv:1808.10806v4. Data availability: "Raw CSD signal of intra-cranial electrode recordings for Fig. 5, Ext. Data Fig. C.3 and Ext. Data Fig. C.4 are available at https://web.gin.g-node.org/zsigmondbenko/intracranial_csd." App. B.2: "CSD was computed (at Fl1, Fl2, iP and Fb), 1–30 Hz Fourier filtering (4th order Butterworth filter) and subsequent rank normalization was carried out on the recordings."

## Method

- Reader: MNE 1.13.2 `read_raw_brainvision` (IEEE_FLOAT_32, resolution 1, empty unit, so MNE reads it as µV). `get_data(units="uV")` is cast back to float32, which gives the stored values exactly. No other scaling.
- Value type per segment: whether all values are integers, min, max, % negative, number of distinct values. A rank transform of a 20480-sample channel would give the positive integers 1..20480.
- Power per channel and segment: `scipy.signal.periodogram` over the full 20 s segment (1024 Hz, 20480 samples, boxcar window, mean removed, 0.05 Hz bins). Power below 1 Hz = sum over 0 < f < 1 Hz / total. Power above 30 Hz = sum over f > 30 Hz / total.

## Result

| run | source CSV | vhdr+eeg == main | Hz | samples x ch | integers | min | max | % < 0 | distinct values | % power < 1 Hz (min-max ch) | % power > 30 Hz (min-max ch) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task-interictal_run-01 | CSD0.csv | True | 1024 | 20480 x 4 | True | -11429 | 10890 | 47.4 | 11769 | 26.0-56.5 | 0.7-2.6 |
| task-interictal_run-02 | CSD10.csv | True | 1024 | 20480 x 4 | True | -8864 | 10978 | 52.6 | 9748 | 28.5-50.6 | 1.0-3.9 |
| task-interictal_run-03 | CSD20.csv | True | 1024 | 20480 x 4 | True | -8369 | 8243 | 51.1 | 9862 | 34.7-57.7 | 1.7-4.1 |
| task-interictal_run-04 | CSD30.csv | True | 1024 | 20480 x 4 | True | -7675 | 7923 | 52.1 | 10320 | 31.9-45.9 | 0.8-4.7 |
| task-interictal_run-05 | CSD50.csv | True | 1024 | 20480 x 4 | True | -9515 | 8796 | 47.4 | 10517 | 33.3-56.1 | 0.6-5.8 |
| task-interictal_run-06 | CSD60.csv | True | 1024 | 20480 x 4 | True | -9155 | 14751 | 51.7 | 10087 | 27.8-50.8 | 1.6-4.2 |
| task-interictal_run-07 | CSD100.csv | True | 1024 | 20480 x 4 | True | -8919 | 17260 | 50.3 | 11249 | 23.9-55.3 | 0.7-4.3 |
| task-interictal_run-08 | CSD110.csv | True | 1024 | 20480 x 4 | True | -9682 | 8721 | 49.2 | 10944 | 31.0-47.0 | 0.5-6.8 |
| task-interictal_run-09 | CSD120.csv | True | 1024 | 20480 x 4 | True | -7902 | 9313 | 48.7 | 10101 | 35.2-58.7 | 0.9-7.8 |
| task-interictal_run-10 | CSD130.csv | True | 1024 | 20480 x 4 | True | -7398 | 6438 | 48.8 | 8557 | 30.2-48.4 | 1.9-8.0 |
| task-interictal_run-11 | CSD140.csv | True | 1024 | 20480 x 4 | True | -6860 | 8086 | 48.0 | 9551 | 32.1-42.1 | 2.9-6.4 |
| task-interictal_run-12 | CSD150.csv | True | 1024 | 20480 x 4 | True | -6791 | 8011 | 52.1 | 8379 | 26.8-42.6 | 2.4-6.6 |
| task-interictal_run-13 | CSD160.csv | True | 1024 | 20480 x 4 | True | -9011 | 9043 | 50.9 | 9817 | 20.9-39.9 | 1.4-4.4 |
| task-interictal_run-14 | CSD170.csv | True | 1024 | 20480 x 4 | True | -9541 | 11019 | 47.4 | 10320 | 28.2-40.2 | 0.7-5.1 |
| task-interictal_run-15 | CSD180.csv | True | 1024 | 20480 x 4 | True | -7202 | 8291 | 48.9 | 9023 | 34.5-53.2 | 2.5-5.8 |
| task-interictal_run-16 | CSD190.csv | True | 1024 | 20480 x 4 | True | -7270 | 8334 | 47.5 | 9218 | 33.5-42.4 | 2.6-7.2 |
| task-seizure_run-01 | CSD2160.csv | True | 1024 | 20480 x 4 | True | -15356 | 25705 | 47.3 | 16295 | 34.2-74.1 | 1.2-23.4 |
| task-seizure_run-02 | CSD2661.csv | True | 1024 | 20480 x 4 | True | -16061 | 23974 | 51.1 | 16447 | 20.9-77.3 | 1.3-13.7 |
| task-seizure_run-03 | CSD3056.csv | True | 1024 | 20480 x 4 | True | -16577 | 33889 | 54.1 | 16418 | 26.0-60.7 | 1.8-18.2 |
| task-seizure_run-04 | CSD3147.csv | True | 1024 | 20480 x 4 | True | -8493 | 27198 | 53.2 | 12294 | 31.8-68.8 | 3.6-55.1 |
| task-seizure_run-05 | CSD3220.csv | True | 1024 | 20480 x 4 | True | -11607 | 22822 | 49.4 | 12094 | 31.8-53.9 | 14.6-44.9 |
| task-seizure_run-06 | CSD3334.csv | True | 1024 | 20480 x 4 | True | -11955 | 21594 | 49.1 | 13222 | 34.7-60.9 | 11.7-38.8 |
| task-seizure_run-07 | CSD3413.csv | True | 1024 | 20480 x 4 | True | -12881 | 11679 | 52.4 | 13169 | 43.0-69.1 | 8.0-41.3 |
| task-seizure_run-08 | CSD3471.csv | True | 1024 | 20480 x 4 | True | -23867 | 21599 | 50.9 | 13875 | 44.4-71.0 | 10.2-25.6 |
| task-seizure_run-09 | CSD3541.csv | True | 1024 | 20480 x 4 | True | -13373 | 17580 | 49.0 | 13184 | 24.3-64.3 | 10.5-25.3 |
| task-seizure_run-10 | CSD3616.csv | True | 1024 | 20480 x 4 | True | -13703 | 18792 | 53.7 | 14591 | 32.4-63.7 | 8.1-16.9 |
| task-seizure_run-11 | CSD3681.csv | True | 1024 | 20480 x 4 | True | -11468 | 17882 | 51.8 | 13326 | 29.6-78.3 | 6.7-31.6 |
| task-seizure_run-12 | CSD3741.csv | True | 1024 | 20480 x 4 | True | -13998 | 24304 | 52.0 | 15246 | 51.6-64.6 | 5.9-18.1 |
| task-seizure_run-13 | CSD3805.csv | True | 1024 | 20480 x 4 | True | -13047 | 24729 | 51.9 | 14840 | 41.6-78.2 | 5.4-25.7 |
| task-seizure_run-14 | CSD3863.csv | True | 1024 | 20480 x 4 | True | -15103 | 24085 | 50.2 | 14402 | 45.9-73.3 | 6.3-20.4 |
| task-seizure_run-15 | CSD3922.csv | True | 1024 | 20480 x 4 | True | -16279 | 19575 | 49.9 | 14829 | 47.6-70.5 | 6.6-18.0 |
| task-seizure_run-16 | CSD3972.csv | True | 1024 | 20480 x 4 | True | -14393 | 14426 | 53.1 | 14867 | 54.8-72.9 | 2.1-24.1 |
| task-seizure_run-17 | CSD4021.csv | True | 1024 | 20480 x 4 | True | -13114 | 17538 | 50.1 | 14141 | 24.1-68.6 | 6.8-22.4 |
| task-seizure_run-18 | CSD4023.csv | True | 1024 | 20480 x 4 | True | -15051 | 15745 | 54.9 | 13314 | 40.9-66.9 | 7.7-26.0 |
Per channel (34 segments each), % of power:

| channel | n | low_min | low_median | low_max | high_min | high_median | high_max |
|---|---|---|---|---|---|---|---|
| GrB6 | 34 | 20.9 | 33.5 | 62.3 | 1.2 | 4.4 | 19.8 |
| GrE2 | 34 | 26.8 | 46.0 | 78.3 | 2.6 | 6.4 | 28.8 |
| GrF4 | 34 | 31.9 | 53.6 | 77.3 | 2.1 | 8.9 | 31.6 |
| FbB3 | 34 | 31.8 | 48.4 | 64.6 | 0.5 | 13.6 | 55.1 |
all 136 channel-segments: % power < 1 Hz 20.9-78.3 (median 46.1); % power > 30 Hz median 6.53 (range 0.5-55.1).

The README's "21-78%" is 20.9-78.3 rounded, and "median 6.5%" is 6.53.

## Coverage

34 of 34 segments (18 seizure, 16 interictal), 4 of 4 channels: 136 channel-segments.

## Reproduce

```
uv run --no-project --with mne==1.13.2 --with scipy --with pandas python code/receipts/2026-10-22_csd-unfiltered.py <nm000394 root> <nm000394 git clone>
```

Run on 2026-10-22 as Slurm job 13448761, with the root `/checkpoint/brainai2/shared/studies/Benko2018Complete/download/nm000394` (NEMAR download, binaries) and a git clone of nemarDatasets/nm000394 (`origin/main` above).
