---
id: natural-sciences.neuroscience.neuroimaging.fmri-preprocessing-and-first-level-analysis
name: fmri-preprocessing-and-first-level-analysis
category: natural-sciences
field: neuroscience
product: neuroimaging
tags: [neuroimaging, neuroscience, fmri, bold, task-fmri, bids, fmriprep, mriqc, preprocessing, motion-correction, framewise-displacement, slice-timing, susceptibility-distortion, fieldmap, normalisation, mni, smoothing, glm, first-level, hrf, design-matrix, confounds, nuisance-regressors, high-pass-filter, contrasts, fsl, spm, afni, nilearn, group-analysis, multiple-comparisons]
level: advanced
status: docs-checked
description: "Preprocess and model task fMRI reproducibly: BIDS, MRIQC and fMRIPrep, motion and confounds, first-level GLM design and contrasts, and group-level multiple-comparison control."
sources: [https://fmriprep.org/en/stable/usage.html, https://fmriprep.org/en/stable/outputs.html, https://mriqc.readthedocs.io/en/stable/, https://nilearn.github.io/stable/modules/generated/nilearn.glm.first_level.FirstLevelModel.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fMRI preprocessing and first-level analysis

**Goal:** go from scanner output to defensible statistical maps for a task fMRI
study, with every step reproducible and quality-checked.

## 1. Before data: design for the analysis
- Pre-register hypotheses, ROIs and the analysis plan where possible.
- **Event timing:** jitter inter-trial intervals (or use an optimised sequence) so
  conditions are separable after HRF convolution; check design efficiency and
  regressor correlations before scanning.
- Acquire **fieldmaps** (or reverse phase-encode pairs) for distortion correction,
  and a T1-weighted anatomical. Record TR, slice order, multiband factor.

## 2. Organise in BIDS
Convert your data to **BIDS** and validate it before running anything: fMRIPrep and
MRIQC both take a BIDS-valid dataset as input (`bids_dir`), with sub-XXXXX folders at
the top level. Keep trial onsets, durations and conditions in the BIDS events files.

## 3. Quality control first
Run **MRIQC**, which extracts no-reference image quality metrics (IQMs) from structural
and functional MRI data. Look for artefacts (ghosting, spikes, signal dropout) and check
**framewise displacement (FD)**. Decide **exclusion criteria before looking at results**;
thresholds vary by study and population, so write down yours and cite the basis.

## 4. Preprocessing with fMRIPrep
`fmriprep <bids_dir> <out_dir> participant --participant-label 01 --fs-license-file <LICENSE>`
The positional arguments are `bids_dir`, `output_dir` and the analysis level, which is
only `participant`. `--participant-label` takes one or more IDs (the `sub-` prefix is
optional) and `--fs-license-file` is the path to a FreeSurfer license key file (free to
register for). Slice-timing correction can be skipped with `--ignore slicetiming`.
Pin the fMRIPrep version you used and report it.
The default volumetric output space is `MNI152NLin2009cAsym` (native `T1w` is also
available). It writes a **confounds TSV** (`desc-confounds_timeseries.tsv`) with: six
rigid-body motion parameters (plus derivatives and quadratic terms for a 24-parameter
set), `framewise_displacement`, `rmsd`, `dvars`, `std_dvars`, `csf`, `white_matter`,
`global_signal`, anatomical and temporal CompCor components (`a_comp_cor_XX`,
`t_comp_cor_XX`), `cosine_XX` regressors, `non_steady_state_outlier_XX` and
`motion_outlier_XX`. It also writes one HTML visual report per subject: **read every
report**. fMRIPrep does not smooth or denoise; you choose that downstream.

## 5. First-level (subject) GLM
- Regressors: each condition's onsets convolved with an HRF model (Nilearn's
  `FirstLevelModel` offers `spm` and `glover` HRFs, each with optional derivative and
  dispersion terms, and `fir`; its default is `glover`).
- Nuisance: motion parameters and CompCor components from the confounds TSV, plus
  motion-outlier regressors for high-FD volumes. Justify every nuisance choice.
- Drift: `FirstLevelModel` defaults to a `cosine` drift model with `high_pass=0.01` Hz;
  set your own cutoff to suit your task period.
- Smoothing: `smoothing_fwhm` is None by default (no smoothing); when set it is in
  millimetres. Choose it to suit the analysis (mass-univariate vs MVPA/ROI).
- Autocorrelation: `noise_model` defaults to `ar1` (the alternative is `ols`).
- Define **contrasts** (e.g. task > baseline, A > B); inspect design matrices for
  collinearity. `fit()` accepts events as a DataFrame or a path to a TSV/CSV file.
Tools: FSL, SPM, AFNI, or Python Nilearn.

## 6. Group level and inference
- Second-level model on subject contrast maps (one-sample, paired, regression with covariates).
- Correct for multiple comparisons with a method valid for your inference (cluster-based
  with a stringent cluster-forming threshold, permutation testing, or voxelwise FWE/FDR);
  state it and cite the tool's documentation.
- Report unthresholded maps and effect sizes, not only blobs.

## Gotchas
- Motion correlated with task (speaking, button presses) creates false activations.
- Circular ROI analysis ("double dipping"): defining an ROI from the same contrast you then test.
- Mixing spaces (native vs MNI) or mismatched TRs between events and data.
- Small samples: underpowered studies produce inflated, unreplicable effects.

## Verify
- [ ] Data in valid BIDS; MRIQC reviewed; exclusions set a priori.
- [ ] fMRIPrep version pinned and every subject's report inspected.
- [ ] Design matrix checked for collinearity; nuisance regressors justified.
- [ ] Group inference uses a valid multiple-comparison method.
- [ ] Pipeline, versions and parameters documented for reproduction.

## Checked
2026-11-01. Confirmed in the fMRIPrep usage and outputs pages: positional arguments,
`--participant-label`, `--fs-license-file`, `--ignore slicetiming`, default output space,
the confounds TSV columns, the per-subject HTML report, and that fMRIPrep does not
smooth or denoise. Confirmed in the MRIQC front page: no-reference IQMs, BIDS input. Confirmed
in the Nilearn `FirstLevelModel` reference: HRF options and default, cosine drift,
`high_pass` 0.01, `noise_model` ar1, `smoothing_fwhm` None, events as DataFrame or file.
Removed: dcm2niix/heudiconv/dcm2bids and BIDS-validator names, the FD and percent-of-volumes
exclusion numbers, the Docker/Singularity recommendation, the fMRIPrep step list
(brain extraction, segmentation, distortion correction), 1/128 Hz drift, 4-8 mm smoothing,
FSL FILM/SPM/AFNI autocorrelation names, the p < 0.001 cluster threshold, randomise/TFCE
and NeuroVault. Experimental-design advice is judgement, not a sourced figure.
Method: documentation only; no commands were run.
