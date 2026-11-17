---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.manure-nutrient-balance-for-land-application
name: manure-nutrient-balance-for-land-application
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, manure-nutrient-balance, nutrient-management-plan, manure-application-rate, nitrogen-availability, phosphorus-index, nitrates-directive, manure-management]
level: advanced
status: draft
description: "Balance manure nutrients against crop needs: lab analysis, plant-available nitrogen, P-based limits, application rate, setbacks, records and regulations to confirm."
sources:
  - "Nitrates Directive 91/676/EEC (https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:31991L0676)"
  - "USDA NRCS Conservation Practice Standard 590 Nutrient Management (https://www.nrcs.usda.gov)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Manure nutrient balance for land application

**Goal:** a field application rate where the manure supplies crop needs without nutrient loss to water or air.

## Steps
1. Crop nutrient requirement: realistic yield goal and the crop's recommended N, P and K rates from soil tests and the local recommendation system, minus credits from previous legumes and residual soil nutrients.
2. Manure nutrient content: lab analysis of a representative sample (total N, ammonium N, P, K, dry matter), updated each year; book values only as fallback (`manure-spreader-types-and-rate-control`).
3. Plant-available N in the first year: ammonium N (less volatilisation depending on the application method, timing and incorporation) plus a fraction of the organic N that mineralises that season. Use the local agency tables for availability factors and volatilisation losses; band or inject manure to reduce ammonia loss.
4. Phosphorus: many plans cap the rate on P, using soil test P and a risk index, or removal by the crop, rather than on N, because manure's N:P ratio is lower than crop need; where soil P is high, application may be restricted.
5. Compute rate = crop need / available nutrient per unit manure, and check the other nutrient limits; supplement with commercial fertiliser to meet the shortfall.
6. Check restrictions: setbacks from water, wells and homes; slope and soil saturation; frozen or snow-covered ground; seasonal bans; annual limits. For example, in EU nitrate vulnerable zones the Nitrates Directive (91/676/EEC, Annex III point 2) limits livestock manure nitrogen to 170 kg N per hectare per year, with derogations granted by the Commission in some regions and a 2026 amendment for processed manure (RENURE) allowing an additional allowance (check OJ L 2026/288); US states and Canadian provinces set their own rules, usually following NRCS Practice Standard 590 or similar. Confirm what applies.

## Records
Keep rates, dates, fields, weather and analysis. Many jurisdictions require a nutrient management plan prepared or approved by a qualified planner.

## Verify
- [ ] Nutrient balance spreadsheet by field, with sources of values.
- [ ] Soil tests after several years confirm P and N trends.
- Unconfirmed: local limits; check the regulator.
