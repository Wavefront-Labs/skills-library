---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.nibp-cuff-pneumatics
name: nibp-cuff-pneumatics
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [bp-cuff, nibp, cuff-sizing, cuff-pneumatics, blood-pressure-cuff]
level: practitioner
status: gated
description: "Design non-invasive blood pressure cuffs and pneumatics: cuff-to-arm sizing, bladder dimensions, pump and valve control, deflation rate, overpressure protection and leaks."
sources: ["AHA scientific statement on measurement of blood pressure in humans (confirm current edition)", "IEC 80601-2-30 Automated non-invasive sphygmomanometers (confirm edition)", "ISO 81060-1 Non-invasive sphygmomanometers (confirm edition)", "https://www.iec.ch"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Cuff sizing and pneumatics

**Goal:** choose a cuff that fits the limb and a pneumatic system that inflates, measures and deflates accurately and safely.

Every figure in this skill (40%/80% bladder rule, 2-3 mmHg/s deflation, 300 mmHg limit) is (gated: unconfirmed, source is paywalled or blocked); the AHA full text returned 403.

## Sizing
- The bladder should encircle most of the arm: the 2019 AHA scientific statement (Muntner et al., Hypertension, Table 2) says bladder length should be 75-100% of arm circumference and width 37-50% (length-to-width ratio 2:1); older guidance quoted about 40% width and 80% length. A cuff too small overestimates BP, too large underestimates.
- Offer several sizes and a means to select (range marks); neonatal and thigh cuffs are separate.

## Pneumatics
1. **Pump and valve:** pump inflates quickly; a proportional bleed valve gives controlled deflation (the AHA statement gives 2 mmHg/s for auscultatory readings and no oscillometric rate; device practice is commonly 2 to 3 mmHg/s (gated: unconfirmed, source is paywalled or blocked)); fast dump valve for safety.
2. **Pressure sensor:** low-noise sensor and amplifier resolving oscillations of fractions of a mmHg on top of the cuff pressure; filter and sample at adequate rate (see oscillometric-algorithm).
3. **Tubing and connectors:** leak-free; compliance of tubing alters oscillation size; connectors per the limb-cuff connector standard (see small-bore-connector-design).
4. **Safety:** independent overpressure protection and a time limit for cuff pressure above a threshold (the standard defines limits for adults, children and neonates; confirm numbers, for example an adult limit near 300 mmHg (gated: unconfirmed, source is paywalled or blocked)).
5. Leak test and calibration against a reference manometer; pressure accuracy tolerance per the standard.

## Verify
- [ ] Cuff bladder dimensions per size comply with the guidance used.
- [ ] Overpressure and dump valve function after single faults.
- [ ] Static pressure accuracy and leak rate meet specification (see bp-validation-iso-81060-2).

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
