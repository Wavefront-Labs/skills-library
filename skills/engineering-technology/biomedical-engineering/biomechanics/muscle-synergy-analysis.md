---
id: engineering-technology.biomedical-engineering.biomechanics.muscle-synergy-analysis
name: muscle-synergy-analysis
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [muscle-synergies, nmf, synergy-analysis, motor-modules, variance-accounted-for]
level: advanced
status: draft
description: "Extract muscle synergies from multi-muscle EMG with non-negative matrix factorisation: preprocessing, rank selection by variance accounted for, stability and reporting."
sources: ["Lee and Seung, Learning the parts of objects by non-negative matrix factorization (Nature, 1999)", "Torres-Oviedo, Macpherson and Ting on synergy extraction (journal literature; confirm citations)", "https://www.isbweb.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Muscle synergy analysis

**Goal:** decompose EMG into a small set of synergies (fixed muscle weightings W) activated by time-varying coefficients C, so EMG is approximately W times C.

## Method
1. Record 8 or more muscles that span the movement; record enough cycles (typically 10 or more) in each condition.
2. Preprocess: band-pass, rectify, low-pass smooth to an envelope (commonly 5-20 Hz cutoff; choose and report; see emg-signal-processing), then normalise each muscle consistently (for example to its maximum or to unit variance), and time-normalise cycles.
3. Concatenate cycles into a matrix D (muscles by time).
4. Use non-negative matrix factorisation (NMF) with the number of synergies k = 1, 2, ... and several random restarts to avoid local minima.
5. **Rank selection:** compute variance accounted for (VAF) and pick the smallest k above a threshold (a commonly used criterion is about 90 percent total VAF) or the elbow in the VAF curve; also test per-muscle VAF.
6. Check stability: split-half or cross-validation, similarity of W between repetitions (scalar product or correlation).
7. Report the processing, k and VAF so others can reproduce.

## Traps
- Different normalisations change the result; synergies are not unique outputs of the nervous system but a mathematical description.
- EMG crosstalk and a poorly chosen muscle set bias k.
- A VAF threshold is a convention, not a law.

## Verify
- [ ] Pipeline, filter cutoffs and normalisation documented.
- [ ] VAF versus k plotted with restarts.
- [ ] Synergy similarity across repeats reported.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
