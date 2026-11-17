---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.oscillometric-algorithm
name: oscillometric-algorithm
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [oscillometric-algorithm, blood-pressure-measurement, oscillometry, nibp, mean-arterial-pressure, cuff-pressure, maximum-amplitude-algorithm]
level: advanced
status: gated
description: "Build an oscillometric blood pressure algorithm: cuff deflation, oscillogram envelope, mean arterial pressure, characteristic ratios and artefact rejection."
sources: ["Geddes et al., Characterization of the oscillometric method for measuring indirect blood pressure (Ann Biomed Eng 1982)", "ISO 81060-1 Non-invasive sphygmomanometers - Requirements and test methods for non-automated measurement type", "ISO 81060-2 Clinical investigation of intermittent automated measurement type (confirm editions)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Oscillometric blood pressure algorithm

**Goal:** estimate systolic, diastolic and mean arterial pressure from cuff pressure oscillations without listening for Korotkoff sounds.

## Signal acquisition
1. Inflate the cuff above expected systolic (use a previous reading or an initial inflation estimate, often 30 mmHg over estimated systolic).
2. Deflate steadily (about 2-3 mmHg per second (gated: unconfirmed, source is paywalled or blocked), or in steps of 4-8 mmHg with a pause to collect beats at each step).
3. Sample the cuff pressure at 100 Hz or more; high-pass (about 0.5 Hz) to extract oscillations, low-pass to the slow cuff pressure.
4. Detect each beat's oscillation peak-to-peak amplitude and the pressure at that point.

## Algorithm (maximum amplitude)
- Build the oscillometric envelope: amplitude versus cuff pressure; smooth with a curve fit.
- **MAP** is the cuff pressure at the maximum oscillation amplitude.
- **Systolic** is the pressure on the high-pressure side where amplitude equals a characteristic ratio (commonly near 0.5-0.6) of the maximum (gated: unconfirmed, source is paywalled or blocked). **Diastolic** is the pressure on the low-pressure side where amplitude equals a ratio (commonly near 0.7-0.8) (gated: unconfirmed, source is paywalled or blocked).
- These ratios are empirical and device-specific, tuned against reference auscultation; other methods use envelope slope or derivative.
- Pulse rate from the beat-to-beat interval.

## Artefact handling
- Reject beats with too-high amplitude change from motion or cuff touch, or irregular rhythm; require a minimum number of valid beats around the maximum; re-inflate if the envelope is poor.
- Atrial fibrillation, arterial stiffness, very low or high pressures and small cuff size reduce accuracy.

## Validation
Clinical validation follows ISO 81060-2 with the required subject numbers and distribution (see bp-validation-iso-81060-2); standard accuracy criteria are mean error and standard deviation limits against reference auscultation.

## Verify
- [ ] Envelope has a clear single peak in clean data.
- [ ] Simulator checks at several pressure points and pulse rates (simulators test hardware only, not clinical accuracy).
- [ ] Artefact flag exercised with motion in bench tests.
