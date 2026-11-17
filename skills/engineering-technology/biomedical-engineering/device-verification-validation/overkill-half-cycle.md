---
id: engineering-technology.biomedical-engineering.device-verification-validation.overkill-half-cycle
name: overkill-half-cycle
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [overkill-method, half-cycle, ethylene-oxide-validation, bi-overkill, sterilization-validation]
level: advanced
status: gated
description: "Validate sterilisation by the overkill (half-cycle) method: biological indicator challenge, fractional cycles, process challenge device and routine cycle with margin."
sources: ["ISO 11135:2014 (+Amd 1:2018) Ethylene oxide; a revision is in progress, check https://www.iso.org/standard/56137.html", "ISO 17665:2024 Sterilization of health care products - Moist heat (https://www.iso.org/standard/80271.html)", "ISO 14937 General requirements for characterization of a sterilizing agent (confirm edition)", "https://www.iso.org/standard/56137.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Half-cycle overkill method

**Goal:** demonstrate that the routine process delivers at least twice the lethality needed to kill a high population of resistant organisms.

## Concept
- The **overkill approach** challenges the process with biological indicators (BIs) containing a high population (commonly 10^6 spores (gated: unconfirmed, source is paywalled or blocked) of a resistant organism; see the standard for the organism per process) placed in the most difficult-to-sterilise locations. The aim is a **half cycle** (half the routine exposure time) that still completely inactivates the BIs, so the full cycle has a large margin.

## Procedure (summary; use the applicable standard for the details)
1. **Define the product family and worst-case load configuration** and the most difficult positions (cold spots, packaging layers, long lumens), based on physical and microbiological mapping.
2. **Place BIs or product inoculated** with the test organism in worst-case positions (inside product or process challenge devices).
3. **Run fractional cycles** to confirm survivors at shorter exposure and show inactivation in the half cycle; typical requirement is repeat demonstration (for example three consecutive cycles) with all BIs negative (gated: unconfirmed, source is paywalled or blocked).
4. **Routine cycle:** set the exposure at least double the half cycle exposure.
5. **Monitor and release:** physical parameters (temperature, humidity, gas concentration, pressure) are recorded; routine BIs or parametric release as allowed.
6. **Requalify** periodically and after product or load changes.

## Traps
- Not testing the true worst-case product and position.
- Loading the BIs where conditions are easier than the product.
- Treating material compatibility at the double exposure as optional (the routine dose must not damage the device; see ethylene-oxide-design and steam-sterilization-design).

## Verify
- [ ] Worst-case locations justified by mapping.
- [ ] Half-cycle results show complete inactivation in the repeats required by the standard.
- [ ] Routine cycle set at twice the half cycle and device functionality verified after it.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
