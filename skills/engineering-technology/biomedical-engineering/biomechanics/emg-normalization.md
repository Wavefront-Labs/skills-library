---
id: engineering-technology.biomedical-engineering.biomechanics.emg-normalization
name: emg-normalization
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [emg-normalization, surface-emg, emg-biomechanics, mvc, maximum-voluntary-contraction, peak-dynamic, isek-standards]
level: practitioner
status: draft
description: "Normalise EMG amplitude with MVC or alternatives: protocol, repeat trials, window selection, dynamic peak method, limitations and reporting per ISEK recommendations."
sources: ["Burden, How should we normalize electromyograms obtained from healthy participants? (J Electromyogr Kinesiol 2010)", "Merletti, Standards for reporting EMG data (J Electromyogr Kinesiol 1999)", "Halaki and Ginn, Normalization of EMG signals: to normalize or not to normalize (in Computational Intelligence in Electromyography Analysis 2012)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# EMG amplitude normalisation

**Goal:** express EMG amplitude relative to a reference so that muscles, sessions and subjects can be compared.

## Methods
- **Maximum voluntary contraction (MVC):** isometric contraction in a standard posture; record 2-3 trials of 3-5 seconds, with rest between, and strong verbal encouragement. Take the highest moving-window RMS (for example 0.5 s window) across trials as 100%.
- **Peak or mean of the dynamic task:** divide by the peak of the ensemble average envelope of the task itself; reduces between-subject variability but removes absolute amplitude information, so cannot compare between conditions with different peaks.
- **Submaximal reference contraction** (for example fixed fraction of body weight) when MVC is unsafe or impossible (pain, patients).
- **M-wave (Mmax)** normalisation in some neurophysiology studies.

## Steps
1. Select MVC tests that elicit maximal activity for each muscle (muscle-specific manoeuvres); some muscles need more than one test.
2. Use the same electrode placement and skin preparation as in the main task; do not move electrodes between MVC and task.
3. Process MVC data with the same filtering and smoothing as the task.
4. Report normalised values as % MVC; values above 100% can occur in dynamic tasks and should be reported, not clipped.
5. State the method, filter settings, window length and number of trials (ISEK reporting standard).

## Cautions
- MVC depends on joint angle, motivation and pain; test-retest reliability varies by muscle.
- Normalised amplitude is not a direct measure of force.
- Comparisons across muscles are not about equal effort.

## Verify
- [ ] MVC reproducibility (the top two trials within about 10% of each other).
- [ ] Normalisation method matches the study question.
- [ ] Methods section lists all reporting items.
