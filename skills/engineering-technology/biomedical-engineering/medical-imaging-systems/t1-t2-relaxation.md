---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.t1-t2-relaxation
name: t1-t2-relaxation
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [t1-t2-relaxation, mri-physics, mri-hardware, larmor-frequency, tr-te, t1-weighted, t2-weighted, proton-density]
level: practitioner
status: docs-checked
description: "Link MRI relaxation to image contrast: Larmor frequency, T1 and T2, typical tissue values by field strength, TR and TE weighting and the engineering consequences."
sources: ["https://physics.nist.gov/cgi-bin/cuu/Value?gammapbar"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# T1 and T2 relaxation and MRI contrast

**Goal:** predict contrast from sequence timing and understand why field strength changes system design.

## Larmor frequency
f = (gamma / 2 pi) x B0, with gamma / 2 pi = 42.577 MHz per tesla for protons (CODATA 2022). 1.5 T gives about 63.9 MHz and 3 T about 127.7 MHz. Hardware (RF coils, amplifiers, cables, shielding) is built for this frequency.

## Relaxation
- **T1 (longitudinal recovery):** spin-lattice; Mz recovers as 1 - exp(-t/T1). T1 of tissue is field-dependent (look up values for your field strength and tissue in a current reference).
- **T2 (transverse decay):** spin-spin; Mxy decays as exp(-t/T2). Measure or look up T2 for your tissue.
- **T2*:** faster decay including field inhomogeneity, used in gradient-echo and susceptibility imaging.
Relaxation values vary with tissue state, temperature and measurement method.

## Contrast from timing (spin echo)
- **T1-weighted:** short TR and short TE; fat bright, fluid dark.
- **T2-weighted:** long TR and long TE; fluid bright.
- **Proton density:** long TR and short TE.
Signal approximation (spin echo): S proportional to PD x (1 - exp(-TR/T1)) x exp(-TE/T2).

## Engineering consequences
- Higher B0 raises signal-to-noise but increases SAR, RF wavelength effects (dielectric shading) and susceptibility artefacts.
- Contrast agents (gadolinium) shorten T1, brightening on T1-weighted images.

## Verify
- [ ] Hand-calculate signal for two tissues at given TR/TE and check against a simulator.
- [ ] Measure T1/T2 of a phantom set and compare with certificate values.

## Checked
2026-11-01. Confirmed: proton gamma / 2 pi = 42.577 478 MHz per tesla (NIST CODATA 2022 page); 63.9 MHz at 1.5 T and 127.7 MHz at 3 T re-computed from it. The recovery and decay forms are standard relaxation equations. Removed: tissue T1 and T2 values and numeric TR/TE windows (no readable source fetched), and the field-dependence claim about T2.
Method: documentation only; no commands were run.
