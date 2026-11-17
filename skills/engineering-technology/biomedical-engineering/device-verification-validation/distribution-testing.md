---
id: engineering-technology.biomedical-engineering.device-verification-validation.distribution-testing
name: distribution-testing
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [distribution-testing, astm-d4169, ista-3a, transit-testing, shipping-simulation]
level: practitioner
status: draft
description: "Simulate shipping and handling for packaged devices: ASTM D4169 and ISTA procedures, test sequence, assurance levels, post-test integrity evaluation and acceptance."
sources: ["ASTM D4169 Performance testing of shipping containers and systems (confirm edition)", "ISTA test procedures (confirm current versions at ista.org)", "ISO 11607-1 (confirm edition)", "https://www.astm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Distribution simulation

**Goal:** show the packaged, sterile device survives the distribution environment with its sterile barrier intact.

## Method
1. **Define the distribution cycle:** shipping modes (parcel, truck, air), handling, storage; choose ASTM D4169 distribution cycle and **assurance level** (I to III, higher severity for riskier shipping), or an ISTA procedure such as ISTA 3A for parcel shipments; use measured data where the real route is harsher.
2. **Test sequence** typically includes conditioning (temperature and humidity), handling drops, stacking or compression, vibration (random vibration in truck mode), low pressure for air shipments, and concentrated impacts; follow the sequence in the chosen standard.
3. **Samples:** final packaged and sterilised product, including shipper carton, as it is distributed; use worst-case configurations (heaviest, largest, minimum protective fill).
4. **Evaluate after testing:** visual inspection of package damage; sterile barrier integrity tests (seal strength, dye penetration, bubble or vacuum decay; see seal-strength-astm-f88 and dye-penetration-astm-f1929); product function inspection.
5. **Acceptance:** predefined criteria for package damage and integrity; report.
6. **Revalidate** when packaging, product weight or distribution changes.

## Verify
- [ ] Test plan names the standard, edition, level and sequence.
- [ ] Post-test integrity tests are validated methods.
- [ ] Worst-case configuration represented.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
