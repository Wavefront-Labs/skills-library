---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.lateral-flow-reader
name: lateral-flow-reader
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [lateral-flow, lateral-flow-reader, test-strip-reader, immunoassay-reader, point-of-care-diagnostic]
level: practitioner
status: draft
description: "Design lateral flow assay readers: optical architecture, lighting control, line quantification, calibration, hook effect and limit of detection, and smartphone readers."
sources: ["Journal literature on lateral flow immunoassay readers (confirm citations)", "CLSI EP standards for evaluation of quantitative methods (confirm current editions)", "https://www.clsi.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Lateral flow readers

**Goal:** turn the colour or fluorescence of the test and control lines into a reliable qualitative or quantitative result.

## Architecture
- **Illumination:** controlled LEDs, enclosed to exclude ambient light; fixed geometry between the strip and the sensor.
- **Detection:** line-scan sensor, camera, or photodiode array for reflectance (colloidal gold lines) or fluorescence readers; smartphone readers use the phone camera with an adapter or reference card.
- **Processing:** locate strip and lines, correct the background, integrate the line intensity, ratio test to control line intensity or to calibrators.

## Performance topics
1. **Limit of detection (LoD)** and cut-off set from dilution series with replicates; report the confidence.
2. **Hook effect:** at very high analyte concentration the signal can fall, giving a false negative or low result; design and label for it (dilution check or two-line approach).
3. **Lot-to-lot variation** of membrane and conjugate: calibration per lot, using barcode or QR coded parameters.
4. **Timing:** read at a defined time after sample application; early or late reads shift intensity.
5. **Result logic and invalid cases:** control line absent, bubble, strip not inserted, flow errors.
6. Software and data connectivity for results reporting; cybersecurity and privacy if connected.

## Verify
- [ ] LoD and cut-off verified with replicates across lots.
- [ ] Invalid-result detection tested.
- [ ] Environmental robustness (temperature, lighting) demonstrated.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
