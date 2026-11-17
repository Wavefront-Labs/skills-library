---
id: engineering-technology.biomedical-engineering.device-verification-validation.cb-scheme-lab-testing
name: cb-scheme-lab-testing
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [cb-scheme, test-laboratory, iecee, national-differences, third-party-testing]
level: practitioner
status: draft
description: "Work with test laboratories for IEC 60601-1 safety and EMC: choosing a lab, CB scheme certificates and national differences, pre-compliance, sample prep and report handling."
sources: ["IECEE CB Scheme documentation (confirm at iecee.org)", "IEC 60601-1 and IEC 60601-1-2 (confirm editions)", "ISO/IEC 17025 (confirm)", "https://www.iecee.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Working with test laboratories (CB scheme)

**Goal:** get test reports and certificates accepted in the target markets with minimal repeated testing.

## Concepts
- The **IECEE CB Scheme** is an international arrangement in which a National Certification Body issues a CB test certificate and report based on IEC standards (including the IEC 60601 series), recognised by member countries, reducing repeat testing. Each country may require national differences testing and its own approval or registration; confirm per market.
- **Accreditation:** use laboratories accredited to ISO/IEC 17025 for the relevant tests, and in the CB scheme a recognised testing laboratory; check the scope covers your standard edition and test types.
- **Regulatory use:** test reports support declarations of conformity; the regulator or notified body decides acceptance; some markets also require local listing (in North America, nationally recognised testing laboratory marks are often requested by purchasers).

## Practice
1. **Pre-compliance testing** in-house or at the lab for EMC and basic safety to find issues before formal testing.
2. **Documentation package:** critical components list with approvals (component certificates reduce testing), schematics, insulation diagram, risk management file summary, essential performance definition, labelling and manuals.
3. **Samples:** production-equivalent, multiple units, with accessories, cables and software versions frozen; destructive tests need extra samples.
4. Agree the test plan with the lab, including edition, collateral standards, essential performance pass criteria and operating modes (worst-case).
5. **Report review:** read the report; check for deviations, national differences and modifications made during testing; keep the report with the design file.
6. **After changes:** assess impact; retest as needed and obtain report amendments.

## Verify
- [ ] Lab accreditation scope covers the tests and standard edition.
- [ ] Final configuration tested matches released design.
- [ ] National differences and market approvals tracked.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
