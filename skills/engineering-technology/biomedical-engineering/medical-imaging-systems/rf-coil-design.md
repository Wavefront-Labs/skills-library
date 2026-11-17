---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.rf-coil-design
name: rf-coil-design
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [rf-coil, mri-coil, birdcage, phased-array, b1-homogeneity]
level: advanced
status: draft
description: "Design MRI RF coils: Larmor frequency, birdcage and surface coils, phased arrays, tuning and matching, transmit-receive detuning, SNR and SAR considerations."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (MRI chapters)", "IEC 60601-2-33 Magnetic resonance equipment for medical diagnosis (confirm edition)", "https://www.ismrm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# RF coil design

**Goal:** a coil that excites uniformly and receives with high SNR, safely.

## Fundamentals
- The proton Larmor frequency is about 42.58 MHz per tesla (about 63.9 MHz at 1.5 T and 127.7 MHz at 3 T).
- **Transmit coils:** the body or head birdcage coil provides a homogeneous B1 field over a large volume (a ladder network of rungs resonant at the Larmor frequency, driven in quadrature for circular polarisation).
- **Receive coils:** surface coils have high local SNR but limited coverage; **phased arrays** combine many small elements; elements are decoupled by overlap and low-impedance preamplifiers.
- **Tuning and matching:** each element tuned to the Larmor frequency and matched to 50 ohm; loading by the patient lowers Q and shifts tuning, so coils are tuned in situ or with a dedicated procedure.
- **Detuning:** receive coils are detuned during transmit (PIN diodes, resonant traps) to avoid induced currents and burns; cable traps (baluns) block common-mode currents on coax cables.

## Safety and performance
- SAR (specific absorption rate) limits for whole-body and local; coil design must keep local hot spots acceptable; at high field (3 T and above), B1 inhomogeneity (dielectric effects) needs care.
- SNR depends on coil size relative to the region of interest, loading, preamp noise figure and number of elements.

## Verify
- [ ] Bench tuning, matching and isolation measured with a network analyser.
- [ ] B1 maps and SNR measured on phantoms.
- [ ] Detuning and cable trap performance verified; SAR assessment complete.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
