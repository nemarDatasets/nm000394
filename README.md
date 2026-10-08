# Intracranial current source density during epileptic seizures (Budapest)

This dataset contains intracranial Current Source Density (CSD) recordings of 18 epileptic seizures and 16 interictal
segments from an epileptic patient (text of the source README).

**This is a derivative dataset.** The signals are current source density traces computed by the data authors from
subdural ECoG; they are not raw electrode voltages. No raw ECoG is part of the source release.

## Source
- G-Node GIN: https://gin.g-node.org/zsigmondbenko/intracranial_csd (commit 3e5bd99b6919d3fa33e8c4d8d50c714f131dc20b, 2018-08-31)
- Copyright (c) 2018 Dániel Fabó and Loránd Erőss, National Institute for Clinical Neurosciences, "Juhász Pál" Epilepsy Center, Budapest, Hungary
- Licence: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (LICENSE copied verbatim)
- Paper that uses these data: Benkő Z. et al., "Complete Inference of Causal Relations between Dynamical Systems", arXiv:1808.10806 (data availability statement points to this repository).

## Recording (from the paper's methods)
A 20-year-old patient with drug-resistant epilepsy underwent subdural grid and strip implantation (ADTECH, 10 mm
inter-contact spacing) for pre-surgical evaluation. Video-EEG was recorded with a Micromed Brain-Quick System Evolution,
referenced to the skull or mastoid, at 1024 Hz. CSD was computed at fronto-lateral (Fl1, Fl2), inferior-parietal (iP)
and fronto-basal (Fb) sites. Patients consented to clinical investigation and surgery along institutional review board
guidelines, in accordance with the Declaration of Helsinki (paper methods).

## Layout
- `sub-01/ieeg/*_task-seizure_run-XX_desc-csd_ieeg.vhdr`: 18 seizure segments (source folder `data/seizure`)
- `sub-01/ieeg/*_task-interictal_run-XX_desc-csd_ieeg.vhdr`: 16 interictal segments (source folder `data/control`)
- each segment: 20480 samples x 4 channels (GrB6, GrE2, GrF4, FbB3); values copied unchanged from the CSV files as float32
- `sub-01/sub-01_scans.tsv`: maps each run to its original CSV file
- `sourcedata/gin-intracranial_csd/`: the complete original repository content (README, LICENSE, CSV files), unchanged

## Not stated by the source (left as n/a)
Units of the CSD values; onset times of the segments; meaning of the numbers in the CSV file names; mapping of the
contact names (GrB6, GrE2, GrF4, FbB3) to the paper's region labels; sex of the patient; filters.

## Additional metadata and localisation (added 2026-10-08)

Compiled after the upload from the article, its supplement and the source deposit (each statement names its source). Text and sidecar metadata only; no data file was changed.

**Processing / reference.** The deposited signals are CSD, not raw potentials: "CSD was computed (at Fl1, Fl2, iP and Fb), 1–30 Hz Fourier filtering (4th order Butterworth filter) and subsequent rank normalization was carried out" (App. B.2, p.28). The deposited CSV values are integers, so whether the stored files are before or after the filtering and rank normalisation is not stated.

**Electrode types.** AD-TECH subdural strips and a grid with 10 mm inter-contact spacing were implanted through a craniotomy, guided by neuronavigation and fluoroscopy (App. B.2). The text describes them as "a subdural grid and two strip electrodes" (p.11).

**Localisation.** Electrodes were identified on the post-implant CT with BioImage Suite, mapped to the pre-implant MRI with FSL FLIRT/BET2, and projected onto the FreeSurfer pial surface (Dykstra et al. 2012). Intraoperative photographs and electrical stimulation mapping (ESM) were used to corroborate the result (App. B.2). The four analysed sites are fronto-basal (Fb), frontal (Fl1), fronto-lateral (Fl2) and infero-parietal (iP), shown on the patient's brain surface in Fig. 5F. Neither coordinates nor the patient MRI are published. Most of the high-frequency seizure activity was in Fb and Fl1. The frontal and fronto-basal regions were resected, and the patient was seizure-free for 1 year before a relapse (p.11).

### Regions per participant (as published; no coordinates exist)

| participant | region (as stated) | hemisphere | contacts | source |
|---|---|---|---|---|
| sub-01 | fronto-basal (Fb) | n/a | 1 (CSD derivation) | arXiv:1808.10806v4, p.11 Results; Fig. 5A/F; App. B.2 |
| sub-01 | frontal (Fl1) | n/a | 1 (CSD derivation) | arXiv:1808.10806v4, p.11 Results; Fig. 5A/F; App. B.2 |
| sub-01 | fronto-lateral (Fl2) | n/a | 1 (CSD derivation) | arXiv:1808.10806v4, p.11 Results; Fig. 5A/F; App. B.2 |
| sub-01 | infero-parietal (iP) | n/a | 1 (CSD derivation) | arXiv:1808.10806v4, p.11 Results; Fig. 5A/F; App. B.2 |
