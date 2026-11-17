---
id: engineering-technology.biomedical-engineering.biomechanics.semg-placement-seniam
name: semg-placement-seniam
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [seniam, surface-emg, emg-biomechanics, electrode-placement, emg-electrodes, skin-preparation]
level: practitioner
status: gated
description: "Place and prepare surface EMG electrodes to SENIAM recommendations: skin prep, size, spacing, muscle belly location, reference electrode and amplifier requirements."
sources: ["Hermens et al., Development of recommendations for SEMG sensors and sensor placement procedures (J Electromyogr Kinesiol 2000)", "SENIAM project recommendations at https://www.seniam.org", "Merletti and Farina, Surface Electromyography: Physiology Engineering and Applications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Surface EMG electrode placement with SENIAM

**Goal:** record repeatable surface EMG that represents the muscle of interest and is not dominated by crosstalk or motion artefact.

The SENIAM recommendations (European project) are widely used guidelines; check the muscle-specific location text on the project site before a study.

## Procedure
1. **Skin preparation:** shave if needed, clean with alcohol, let dry; light abrasion if impedance is high. Good practice is to measure skin impedance and keep it low and similar between electrodes.
2. **Electrode choice:** bipolar Ag/AgCl, small (SENIAM muscle pages, for example biceps femoris: maximum electrode size 10 mm along the fibres, electrode distance 20 mm; the one-quarter-of-fibre-length rule for short muscles (gated: unconfirmed, source is paywalled or blocked)).
3. **Location:** on the line between the origin and insertion, over the muscle belly and away from the innervation zone and tendon ends; follow the muscle-specific descriptions (subject position, palpation tests).
4. **Orientation:** electrode pair parallel to muscle fibres.
5. **Reference electrode** on an electrically neutral, bony site (SENIAM biceps femoris page: on or around the ankle or the spinous process of C7; other muscles may differ, check the muscle page) away from the muscles under study.
6. **Cables:** tape or use wearable pre-amplifiers; secure leads to reduce movement artefact.
7. **Amplifier** (typical values, not confirmed against SENIAM (gated: unconfirmed, source is paywalled or blocked)): high input impedance (well above electrode impedance), CMRR above 100 dB, low noise (around 1 microvolt rms in-band), bandwidth roughly 10-500 Hz; sample at no less than twice the highest frequency kept (1 kHz or higher is typical).
8. **Check:** ask for a known contraction and view the raw trace for clean baseline and no mains.

## Gotchas
- Crosstalk from neighbouring muscles: reduce inter-electrode distance and verify with test movements.
- Placement drifts during dynamic tasks; re-check after movement trials.
- Mains pickup means shielding, short leads and an equal electrode impedance.

## Verify
- [ ] Baseline noise measured at rest.
- [ ] Targeted manoeuvre produces largest signal in the intended channel.
- [ ] Placement photographed or marked for repeat sessions.
