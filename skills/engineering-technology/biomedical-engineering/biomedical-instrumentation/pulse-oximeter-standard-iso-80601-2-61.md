---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.pulse-oximeter-standard-iso-80601-2-61
name: pulse-oximeter-standard-iso-80601-2-61
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [iso-80601-2-61, pulse-oximeter-standard, spo2-accuracy-test, arms, desaturation-study]
level: advanced
status: gated
description: "Plan ISO 80601-2-61 pulse oximeter accuracy testing: induced hypoxia study design, reference co-oximetry, ARMS analysis, subject requirements and the other clauses to cover."
sources: ["ISO 80601-2-61 Medical electrical equipment - Particular requirements for basic safety and essential performance of pulse oximeter equipment (confirm edition and amendments)", "FDA guidance Pulse Oximeters - Premarket Notification Submissions [510(k)s], issued 4 March 2013 (https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pulse-oximeters-premarket-notification-submissions-510ks-guidance-industry-and-food-and-drug); check fda.gov for any newer or draft revision", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ISO 80601-2-61 accuracy testing

**Goal:** demonstrate SpO2 accuracy against arterial blood co-oximetry using the standard's method.

## Method (summary; use the standard text)
1. **Induced hypoxia study:** healthy volunteers breathe controlled gas mixtures to reach several stable saturation plateaus across the claimed range (the FDA 2013 guidance evaluates from about 70 to 100 percent SpO2), with arterial blood samples drawn at each plateau and analysed on a laboratory co-oximeter as the reference.
2. Sensor and monitor are placed per instructions; readings are matched in time with samples.
3. **ARMS (accuracy root mean square)** is computed over the pairs; FDA 2013 guidance recommends an ARMS specification consistent with ISO 80601-2-61, evaluated from about 70% to 100% SpO2, with typical values of at most 3.0% for transmittance, wrap and clip sensors and at most 3.5% for ear clip and reflectance sensors (fetched from the FDA page). The ISO text itself (gated: unconfirmed, source is paywalled or blocked); confirm the limits for your edition and probe type.
4. **Subjects:** the FDA 2013 guidance recommends 10 or more healthy subjects varying in age and sex, at least 200 paired data points, and a range of skin pigmentations including at least 2 darkly pigmented subjects or 15% of the pool, whichever is larger. Confirm the ISO edition rule and any newer FDA guidance.
5. **Other requirements:** alarm systems, response to low perfusion, behaviour under motion, and for home use the relevant collateral standard (see home-healthcare-environment).
6. Document protocol, arterial line procedure, ethics approval and the data analysis.

## Verify
- [ ] Study design reviewed against the current standard text and regulator guidance.
- [ ] Co-oximeter calibration and sampling traceable.
- [ ] Results reported per subgroup as well as pooled.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
