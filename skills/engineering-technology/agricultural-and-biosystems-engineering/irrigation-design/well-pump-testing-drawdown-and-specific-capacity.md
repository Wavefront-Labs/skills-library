---
id: engineering-technology.agricultural-and-biosystems-engineering.irrigation-design.well-pump-testing-drawdown-and-specific-capacity
name: well-pump-testing-drawdown-and-specific-capacity
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: irrigation-design
tags: [agricultural-and-biosystems-engineering, irrigation-design, well-drawdown-test, irrigation-pumping, pump-selection, step-drawdown, specific-capacity, constant-rate-test, cooper-jacob, aquifer-test]
level: practitioner
status: draft
description: "Test an irrigation well with step-drawdown and constant-rate tests, compute specific capacity and aquifer parameters, and size the pump setting below the pumping level."
sources:
  - "USDA NRCS National Engineering Handbook, Part 623 Irrigation (https://www.nrcs.usda.gov)"
  - "Keller & Bliesner, Sprinkle and Trickle Irrigation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Well pump testing, drawdown and specific capacity

**Goal:** the yield you can rely on in a dry season and the pump setting depth that avoids dewatering.

## Tests
1. **Step-drawdown**: pump at 3-5 increasing rates, each for a fixed time (often 1-2 hours), measuring drawdown at the end of each step with an electric water-level probe. Plot specific drawdown s/Q versus Q to separate linear (aquifer) loss from well loss.
2. **Constant-rate test**: pump at a steady rate for 24-72 hours (as required by permit or hydrogeologist), measuring drawdown and recovery. Analyse with the Cooper-Jacob straight-line method (semi-log plot of drawdown versus time) for transmissivity.
3. **Specific capacity** = Q / s (m3/h per m of drawdown); it falls with pumping time and with seasonal water level declines.

## Pump setting
- Pumping level = static level (worst-case season low) + projected long-term drawdown at the design flow + interference from nearby wells.
- Set the pump intake below the pumping level by at least the NPSH requirement plus a safety margin (often several metres), and above the screen top or well bottom.
- Water quality: sand production requires changing the well design or slower rates.

## Regulatory
Well construction, testing and abstraction are regulated; a licensed driller or hydrogeologist is usually required, and water-right measurement and reporting apply.

## Gotchas
- Pumping interference between wells reduces yield.
- Drawdown measured during a wet season overstates dry-season capacity.

## Verify
- [ ] Recovery data confirms the aquifer returns to the static level.
