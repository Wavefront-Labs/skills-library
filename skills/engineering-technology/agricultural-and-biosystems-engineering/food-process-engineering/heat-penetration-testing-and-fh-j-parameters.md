---
id: engineering-technology.agricultural-and-biosystems-engineering.food-process-engineering.heat-penetration-testing-and-fh-j-parameters
name: heat-penetration-testing-and-fh-j-parameters
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: food-process-engineering
tags: [agricultural-and-biosystems-engineering, food-process-engineering, heat-penetration-test, thermal-processing, canning-process, fh-value, j-factor, cold-spot, thermocouple, come-up-time]
level: practitioner
status: verified
description: "Run a heat penetration test with thermocouples at the cold spot, plot the semi-log heating curve, and extract fh, jch and come-up-time corrections for process calculation."
sources:
  - "Toledo, Fundamentals of Food Process Engineering"
  - "Singh & Heldman, Introduction to Food Engineering"
  - "US FDA food safety regulations (https://www.fda.gov)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Heat penetration testing and fh/j parameters

**Goal:** a reliable time-temperature record at the slowest heating point to support a scheduled process.

## Setup
1. Identify the cold spot: geometric centre for conduction-heating products; a point slightly below centre for convection-heating products in still retorts (verify experimentally).
2. Use calibrated thermocouples or wireless data loggers with fittings that do not alter heat flow (needle thermocouples through packing glands, or in-container loggers). Calibrate at ice point and at a high reference temperature; record uncertainty.
3. Test worst-case: largest container, highest viscosity or fill weight, coldest initial temperature, product in the lowest-expected-agitation condition, worst retort load position.
4. Use enough replicates across the retort load (often 10-20 (gated: unconfirmed, source is paywalled or blocked)); 21 CFR 113 sets no number, so follow the process authority's protocol.

## Analysis
- Plot `log (T_retort - T_product)` versus time on semi-log axes; the straight portion has slope giving `fh` (minutes per log cycle).
- `j_ch = (T_retort - T_pih) / (T_retort - T_ih)` where T_pih is the extrapolated intercept at time zero (pseudo-initial temperature) and T_ih the actual initial temperature.
- Account for the retort come-up time (CUT): Ball's method takes the effective start of heating (zero time) as 58 percent of CUT after steam-on, so the plotted time axis is shifted accordingly.
- Broken heating curves (starch gelatinisation, fat melting) need two slopes (fh1, fh2).

## Gotchas
- Poor thermocouple placement dominates errors; verify by x-ray or sectioning.
- Retort temperature distribution must be demonstrated separately.
- Low-acid canned food process establishment is regulated (21 CFR Part 113 low-acid and Part 114 acidified foods in the US); the process authority designs and approves the process.

## Verify
- [ ] Replicate curves overlap; slowest curve used for process calculation.
