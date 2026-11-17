---
id: engineering-technology.chemical-engineering.process-safety.toxic-exposure-and-probit
name: toxic-exposure-and-probit
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-consequence-modelling, toxic-exposure-and-probit, toxic-exposure, probit, dose-response, erpg, aegl, idlh, toxic-load, consequence-assessment, toxic-release]
level: advanced
status: gated
description: "Assess toxic exposure with concentration-time criteria (ERPG, AEGL, IDLH) and probit dose-response, with caution on constants and averaging time."
sources:
  - "https://www.epa.gov/aegl/about-acute-exposure-guideline-levels-aegls"
  - "https://www.aiha.org/get-involved/aiha-guideline-foundation/erpgs"
  - "https://www.cdc.gov/niosh/idlh/intridl4.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Toxic exposure and probit analysis

**Goal:** translate a dispersion result (concentration versus time) into health effects and hazard distances. Guidelines and constants must come from current authoritative sources; confirm the current values for the substance and jurisdiction.

## Exposure guideline values (use the current published tables)
- **AEGL** (US Acute Exposure Guideline Levels, published on the EPA AEGL pages; AEGL-1 mild reversible effects, AEGL-2 serious or irreversible effects or impaired ability to escape, AEGL-3 life-threatening effects or death, each for 10 min, 30 min, 1 h, 4 h and 8 h).
- **ERPG** (AIHA Emergency Response Planning Guidelines, ERPG-1, -2, -3 for brief single airborne exposures; the one-hour basis is the usual convention (gated: unconfirmed, source is paywalled or blocked)).
- **IDLH** (NIOSH immediately dangerous to life or health values).
- Local regulatory limits (occupational exposure limits are for working life exposures and are not emergency criteria).
Select the criterion required by the study or regulator (for example for land-use planning or emergency planning zones).

## Probit method
The probit Pr relates dose to probability of a response: Pr = a + b ln(C^n t), with C the concentration, t the exposure time, and a, b, n substance-specific constants from published tables. Convert probit to probability (Pr = 5 corresponds to 50%, Pr about 6.28 to 90%; computed as 5 + z with z from the standard normal, 5 + 1.2816 = 6.2816 for 90%) using the normal distribution.
Do not use constants from memory; obtain them from CCPS, Crowl and Louvar or the national guidance, and note the units (ppm and minutes versus mg/m3 and seconds).

## Procedure
1. Compute the concentration-time profile at each receptor from the dispersion model (the toxic load is the integral of C^n dt).
2. Compute the probit and probability of fatality or of the chosen effect.
3. Apply indoor shelter factors if sheltering is the response, and the effect of escape.
4. Produce a risk contour or distances to criteria.

## Gotchas
- The averaging time of the dispersion model must match the criterion time basis.
- A model producing a high instantaneous peak with very short duration can overstate the dose; compute the dose, not just the peak.
- Probit constants are derived from limited animal data; treat the results as indicative.

## Verify
- [ ] Constants and their reference recorded with units.
- [ ] Sensitivity to the exponent n and to weather presented.
