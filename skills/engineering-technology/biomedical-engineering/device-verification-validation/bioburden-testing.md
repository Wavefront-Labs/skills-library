---
id: engineering-technology.biomedical-engineering.device-verification-validation.bioburden-testing
name: bioburden-testing
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [bioburden, sterilization-validation, sal, iso-11737-1, recovery-efficiency, bioburden-limits, aerobic-count, spore-count]
level: practitioner
status: gated
description: "Determine product bioburden per ISO 11737-1: sampling, extraction and recovery validation, culture conditions, correction factor, action levels and dose audit links."
sources: ["ISO 11737-1 Sterilization of health care products - Microbiological methods - Determination of a population of microorganisms on products (confirm edition)", "ISO 11737-2 Tests of sterility performed in the definition validation and maintenance of a sterilization process"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Bioburden testing

**Goal:** count viable microorganisms on a product before sterilisation so the sterilisation process (EO, radiation, steam) is justified and monitored.

Regulated microbiological work; laboratory and acceptance details follow ISO 11737-1 and your sterilisation standard (confirm editions).

## Plan
1. **Sample selection:** representative products from production lots over time (for routine monitoring, many manufacturers test each lot or a periodic schedule based on history); include worst-case products or families if justified by a family-grouping rationale.
2. **Sample handling:** test items in their finished form before sterilisation, without disinfection; take samples aseptically from the production environment and keep time to test short.

## Method
- **Extraction:** immerse or rinse the product in a validated diluent (peptone-saline with surfactant) with shaking, stomaching, or ultrasonics; for large items test portions or the whole item.
- **Enumeration:** membrane filtration or pour plate; incubate aerobic counts on tryptic soy agar at about 30-35 C for roughly 3-5 days and fungi on Sabouraud agar at about 20-25 C for roughly 5-7 days (confirm the plan's conditions (gated: unconfirmed, source is paywalled or blocked)).
- Report CFU per product (and, for radiation dose setting, the spore subset after a heat shock of about 80 C for 10 min (gated: unconfirmed, source is paywalled or blocked)).

## Recovery efficiency (validation)
- **Repeat recovery:** extract the same product several times; the sum of counts relative to the first extraction gives the efficiency.
- **Inoculated product:** add a known number of organisms and measure what is recovered.
- Apply the **correction factor** from validation to results (where the standard permits) and include method suitability (the product extract must not inhibit growth).

## Use of the results
- Set alert and action levels from historical data; investigate excursions (cleanroom, materials, personnel).
- Link to the sterilisation process: ISO 11135 EO validation and radiation dose setting methods use bioburden as an input (see vdmax-dose-setting).
- Identify organisms from high counts to look for resistance or contamination sources.

## Verify
- [ ] Recovery validation documented and repeated when product or extraction changes.
- [ ] Negative controls clean at each test.
- [ ] Trend charts reviewed in management reviews.
