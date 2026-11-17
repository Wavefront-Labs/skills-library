---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.ten-twenty-montage
name: ten-twenty-montage
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [ten-twenty-system, eeg, eeg-acquisition, 10-20-system, electrode-placement-eeg, montage, bipolar-montage, referential-montage]
level: practitioner
status: gated
description: "Apply the 10-20 EEG system: landmark measurement, electrode naming and positions, reference and bipolar montages, 10-10 extension and typical hardware setup."
sources: ["Klem et al., The ten-twenty electrode system of the International Federation of Clinical Neurophysiology (Electroencephalogr Clin Neurophysiol Suppl 1999;52:3-6)", "American Clinical Neurophysiology Society, Guidelines for standard electrode position nomenclature and EEG montages (current versions) at https://www.acns.org", "Niedermeyer and Lopes da Silva, Electroencephalography: Basic Principles Clinical Applications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# 10-20 electrode system and montages

**Goal:** place EEG electrodes at reproducible scalp positions and display channels with a montage that suits the clinical or research question.

## Landmarks and placement
1. Measure nasion-to-inion along the midline and mark points at 10%, 20%, 20%, 20%, 20%, 10% of the distance; Fpz, Fz, Cz, Pz, Oz fall on the midline.
2. Measure the preauricular points (ear to ear) through Cz and mark 10% and 20% intervals for the T, C, and neighbouring positions.
3. Name: letters F, C, P, T, O, Fp for frontal, central, parietal, temporal, occipital and frontal pole; **odd numbers on the left, even on the right, z on the midline**. Older T3, T4, T5, T6 are now T7, T8, P7, P8 in the extended nomenclature (gated: unconfirmed, source is paywalled or blocked).
4. The **10-10** system adds intermediate electrodes for 64 or more channels (gated: unconfirmed, source is paywalled or blocked); high-density caps follow equidistant layouts.

## Montages
- **Referential:** each channel against a common reference (for example Cz, linked mastoids, or average reference); shows absolute amplitude and spatial distribution.
- **Bipolar:** adjacent electrode pairs in chains (the "double banana" longitudinal and transverse chains) show phase reversal at a focus.
- **Laplacian and average** montages enhance local activity.

## Practical setup
- Ground and reference electrodes are chosen by the system; the common mode sense and drive electrodes should be on the forehead or mastoid.
- Check impedance before recording (see eeg-impedance-checking).
- Use head circumference to choose cap size and verify Cz location.

## Verify
- [ ] Electrode labels match the montage definitions in the software.
- [ ] Symmetric electrode positions left to right.
- [ ] Recorded test (eyes open and closed) shows alpha posteriorly on eye closure.
