---
id: engineering-technology.biomedical-engineering.device-verification-validation.seal-strength-astm-f88
name: seal-strength-astm-f88
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [seal-strength, packaging-validation, shelf-life, packaging-shelf-life, astm-f88, peel-test, tensile-tester, iso-11607-2]
level: practitioner
status: gated
description: "Measure seal strength of flexible packaging per ASTM F88: specimen cutting, conditioning, test speed, fixture techniques A B C, reported values and typical acceptance practice."
sources: ["ASTM F88/F88M Standard test method for seal strength of flexible barrier materials (confirm current edition)", "ASTM F1886 Visual inspection of seals in medical device packaging", "ISO 11607-2 Packaging for terminally sterilized medical devices - Validation requirements for forming sealing and assembly processes"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Seal strength (ASTM F88)

**Goal:** quantify the peel force of heat seals and support the packaging process validation.

## Method outline
- **Specimens:** strips cut perpendicular to the seal, typically 25.4 mm (1 inch) or 15 mm wide, long enough to grip both tails; cut with a precision cutter or die to avoid edge damage.
- **Conditioning:** at about 23 C and 50% relative humidity for at least 40 hours before testing (gated: unconfirmed, source is paywalled or blocked), and test at the same temperature.
- **Test equipment:** a tensile tester with a load cell appropriate for the expected force (forces within 10-90% of range), pneumatic grips and a calibrated speed.
- **Rate of separation:** about 300 mm/min (12 in/min (gated: unconfirmed, source is paywalled or blocked)); some products specify others.
- **Fixtures:**
  - **Technique A:** unsupported tails (T-peel), the tails held in the grips by the operator or free.
  - **Technique B:** 90-degree supported peel for example with a fixture.
  - **Technique C:** 180-degree supported peel (the tail is folded back).
  Choose the technique and keep the same for comparisons.

## Procedure
1. Measure at least 5-10 specimens per lot or per sample location (all sides of a pouch, tray corners, different sealer cavities).
2. Record **peak force**, **average force** over the peel (after the initial rise) and the failure mode: adhesive peel, cohesive failure, delamination, material tear or film break.
3. Report in N per 15 mm width or N per 25.4 mm, with mean, standard deviation, minimum.
4. Photograph samples and fracture surfaces.

## Acceptance
ISO 11607-1 does not set a universal number (gated: unconfirmed, source is paywalled or blocked); manufacturers set a minimum based on process capability and package performance, with commonly used internal minimums around 1 lbf/in (about 2.6 N per 15 mm; 4.448 N/lbf x 15/25.4 = 2.63 computed) for peelable seals, plus a maximum to ensure peelability without fibre tear or delamination. Justify limits with distribution and ageing data.

## Pitfalls
- Wrong speed or sample width; load cell range too large.
- Mixed failure modes need interpretation: material tear (stronger than seal) is not a seal defect.
- Gripping artefacts and curling.

## Verify
- [ ] Test equipment calibrated; speed checked.
- [ ] Sample plan covers seal geometry and process window extremes in OQ.
- [ ] Results after sterilisation and ageing meet the same criteria.
