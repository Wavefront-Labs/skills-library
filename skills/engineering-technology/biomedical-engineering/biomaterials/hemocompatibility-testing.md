---
id: engineering-technology.biomedical-engineering.biomaterials.hemocompatibility-testing
name: hemocompatibility-testing
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [hemocompatibility, foreign-body-response, protein-adsorption, host-response, iso-10993-4, hemolysis, astm-f756, thrombogenicity, complement-activation]
level: practitioner
status: verified
description: "Plan ISO 10993-4 haemocompatibility testing: test categories, haemolysis, platelet, coagulation and complement assays, in vivo thrombogenicity and interpretation traps."
sources: ["ISO 10993-4 Biological evaluation of medical devices - Selection of tests for interactions with blood (confirm edition)", "ASTM F756 Standard practice for assessment of hemolytic properties of materials (confirm edition)", "FDA guidance on use of ISO 10993-1 (current text at https://www.fda.gov)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Haemocompatibility testing (ISO 10993-4)

**Goal:** choose and run the blood-interaction tests that match the device's blood contact and duration.

Biological evaluation is planned within ISO 10993-1 and a biological evaluation plan reviewed by a toxicologist; confirm editions and FDA or EU expectations.

## Step 1: does the device need it?
Devices that contact circulating blood (external communicating, or implants in the blood path) normally need evaluation; the extent depends on contact (limited, prolonged, permanent) and the risk.

## Test categories in ISO 10993-4
- **Thrombosis:** device-related clot formation, in vivo (animal implant or ex vivo shunt) or in vitro dynamic flow loops.
- **Coagulation:** partial thromboplastin time and related assays on contacted plasma or blood.
- **Platelets:** counts and activation markers after contact.
- **Haematology:** leukocyte counts and haemolysis.
- **Complement system:** activation products (for example C3a, SC5b-9) for devices with prolonged blood contact.

## Common in vitro tests
- **Haemolysis (ASTM F756):** direct contact and extract methods with rabbit or human blood; haemolytic index typically graded as non-haemolytic (up to 2%), slightly haemolytic (2-5%), haemolytic (above 5%) (gated: unconfirmed, source is paywalled or blocked); use positive and negative controls.
- Use the **final sterilised device** and extraction ratio per ISO 10993-12.
- Blood donors and anticoagulant (heparin or citrate) matter; run controls in the same blood.

## Interpretation traps
- In vitro results do not guarantee in vivo non-thrombogenicity; static tests have limited relevance for flow devices, so dynamic tests are preferred.
- Coatings (heparin, phosphorylcholine) must be tested after sterilisation and ageing.
- Platelet and complement results vary by donor; use several donors.

## Verify
- [ ] Biological evaluation plan identifies blood-contact category and tests.
- [ ] Controls pass and donor variability addressed.
- [ ] Reports from an ISO 17025 and GLP-compliant laboratory where required.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
