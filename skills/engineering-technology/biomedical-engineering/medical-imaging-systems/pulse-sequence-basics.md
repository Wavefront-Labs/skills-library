---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.pulse-sequence-basics
name: pulse-sequence-basics
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [pulse-sequence, spin-echo, gradient-echo, inversion-recovery, tr-te]
level: practitioner
status: verified
description: "Understand the basic MRI pulse sequences (spin echo, gradient echo, inversion recovery, EPI): timing parameters, contrast weighting, flip angle and Ernst angle."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (MRI sequence chapters)", "Prince and Links, Medical Imaging Signals and Systems", "https://www.ismrm.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pulse sequence basics

**Goal:** know how sequence parameters set contrast, speed and artefacts, for design, QA and safety discussion.

## Sequences
- **Spin echo (SE):** a 90 degree excitation then a 180 degree refocusing pulse; echo at TE. Corrects static field inhomogeneity; the contrast follows T1 (short TR, short TE), T2 (long TR, long TE) or proton density (long TR, short TE).
- **Gradient echo (GRE):** excitation with flip angle alpha, the echo made by gradient reversal; faster, but sensitive to field inhomogeneity (T2 star). Contrast depends on TR, TE and flip angle. The **Ernst angle** maximising steady signal satisfies cos(alpha) = exp(-TR / T1) (checked numerically by maximising sin(a)(1-E)/(1-E cos a), E = exp(-TR/T1), for TR/T1 = 0.05, 0.3 and 1). For TI, the longitudinal magnetisation after a 180 degree pulse with long TR is 1 - 2 exp(-TI/T1), zero at TI = T1 ln 2 (0.693 T1, solved numerically).
- **Inversion recovery (IR):** a 180 degree pulse then a delay TI before excitation; choosing TI nulls a tissue (about T1 times ln 2 for a long TR), as in FLAIR (fluid) and STIR (fat).
- **Echo planar imaging (EPI):** many echoes after one excitation for very fast imaging (functional and diffusion); distortions and gradient demands are high.
- **Fast or turbo spin echo:** several refocused echoes per TR to shorten scans.

## Parameter effects
- TR sets T1 weighting and scan time; TE sets T2 weighting; flip angle changes T1 sensitivity; bandwidth trades SNR and chemical shift; matrix and field of view set resolution (see k-space-sampling).
- SAR rises with 180 degree pulses and high flip angles; sequences are tuned within SAR limits.

## Verify
- [ ] Calculate Ernst angle for example tissue T1 values with a test script.
- [ ] Phantom contrast behaves as predicted when TR and TE are changed.
- [ ] SAR and gradient limits checked for the chosen sequence.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
