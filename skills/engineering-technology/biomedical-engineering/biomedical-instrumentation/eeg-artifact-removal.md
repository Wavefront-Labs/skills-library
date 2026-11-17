---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.eeg-artifact-removal
name: eeg-artifact-removal
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [eeg-artifact, artifact-removal, ica, eog-artifact, eeg-preprocessing]
level: advanced
status: gated
description: "Remove EEG artefacts (blink, movement, muscle, line noise, electrode pops) with filtering, regression, ICA and artefact-subspace methods without distorting neural signals."
sources: ["Delorme and Makeig, EEGLAB: an open source toolbox for analysis of single-trial EEG dynamics (J Neurosci Methods, 2004)", "IFCN guidelines on clinical EEG (confirm current version)", "https://sccn.ucsd.edu"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EEG artefact removal

**Goal:** clean EEG for the intended analysis while documenting what was removed.

## Artefact types and handling
- **Eye blink and movement (EOG):** large frontal low-frequency potentials (tens to hundreds of microvolts). Handle by regression on EOG channels, or **independent component analysis (ICA)** to find and remove blink components.
- **Muscle (EMG):** broadband high-frequency contamination, strongest in temporal and frontal channels; reduce with filters, ICA or by rejecting segments; hard to remove fully.
- **Line noise (50 or 60 Hz):** notch filter or adaptive removal; first fix cause (see mains-interference-filtering).
- **Electrode pops, cable motion, baseline wander:** reject segments or interpolate bad channels; high-pass filter (about 0.1 to 1 Hz depending on analysis).
- **ECG and pulse artefact:** component removal or template subtraction.

## Pipeline sketch
1. Inspect raw data; mark bad channels and segments.
2. Filter (high-pass, notch), re-reference (average or linked mastoids by protocol).
3. Run ICA on filtered data (high-pass of about 1 Hz often improves ICA) (gated: unconfirmed, source is paywalled or blocked); identify artefact components by topography, spectrum and time course (automatic classifiers help but review them).
4. Subtract the artefact components; interpolate removed channels; re-check.
5. Log all steps for reproducibility; do not remove neural signal of interest (for example high-frequency analysis).

## Verify
- [ ] Before and after spectra and epochs inspected.
- [ ] Number of rejected components and segments reported.
- [ ] Pipeline script archived.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
