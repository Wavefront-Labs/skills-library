---
id: hospitality-culinary.food-preservation.curing.equilibrium-curing-and-nitrite-calculation
name: equilibrium-curing-and-nitrite-calculation
category: hospitality-culinary
field: food-preservation
product: curing
tags: [curing, dry-curing, equilibrium-curing, wet-curing, brining, brine, cure-calculation, curing-salt, prague-powder, pink-salt, cure-1, cure-2, sodium-nitrite, sodium-nitrate, ppm, bacon, pancetta, coppa, bresaola, gravlax, salt-fish, lox, charcuterie, salumi, botulism, water-activity, food-preservation]
level: practitioner
status: docs-checked
description: "Salt-curing meat and fish: equilibrium-cure maths by weight, curing salt #1 vs #2 dosing, brine strength, cure times, weight-loss targets and nitrite safety."
sources:
  - "https://www.ecfr.gov/current/title-9/part-424/section-424.21"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Equilibrium curing and nitrite calculation

**Goal:** cure meat or fish so it is seasoned evenly, never over-salted, and dosed with
nitrite inside safe limits — by calculating everything as a percentage of total weight.

## 1. Equilibrium curing (EQ) — the method
Weigh the meat (and water, if brining). Salt and cure are computed against that weight, so
the product can sit in the cure "too long" without becoming saltier than intended.
- **Salt and sugar (optional):** set as a percentage of meat weight from a tested recipe, and write them down.
- **Curing salt #1** (6.25 % sodium nitrite, rest salt): **0.25 % of meat weight**
  = 2.5 g/kg → 0.0156 % sodium nitrite, i.e. ~156 ppm ingoing nitrite, which equals the US 9 CFR 424.21 chart limit of
  1/4 oz sodium nitrite per 100 lb of chopped meat. For short cures that will be cooked or
  hot-smoked: bacon, ham, sausages, pastrami.
- **Curing salt #2** (contains nitrate as well as nitrite; follow the product label) is used for long air-dried
  products, where the nitrate slowly converts to nitrite.
- Worked example, 2,000 g pork belly at 2.25 % salt, 1 % sugar, cure #1:
  salt 45 g, sugar 20 g, cure #1 5 g. (Strictly, the cure's own salt counts toward the
  total; at this dose it's ~4.7 g, so purists drop the added salt to ~40 g.)
- Vacuum-bag or zip-bag tightly, keep refrigerated and flip daily; take the cure time from a tested recipe for the thickness.

## 2. Wet curing (brines)
Calculate on **meat + water** weight for EQ. Traditional (non-EQ) brines are stronger
and need timed removal and rinsing. Keep brines cold.

## 3. Fish: quick salt cures
Gravlax is a short refrigerated salt-and-sugar cure of skin-on salmon, then rinsed; follow a tested recipe.
**Parasite risk:** fish eaten without cooking may need to be frozen first; follow your national regulator's freezing time and temperature.

## 4. Nitrite safety
- Nitrite blocks *Clostridium botulinum* in anaerobic, slow-dried or smoked products and
  gives the pink colour and "cured" flavour.
- It is **toxic in excess**. Store curing salt separately from table salt, labelled and away from children.
- Never use a recipe that gives cure by volume without weight; a miscalculation by a
  decimal place is a poisoning risk. Use a 0.01 g scale for small batches.
- Regulatory ceilings differ by country and product class. In the US, 9 CFR 424.21 caps nitrite at 200 ppm in the finished
  product (bacon is handled under its own paragraph); check your jurisdiction if selling.

## 5. Air-drying whole muscle (after curing)
Rinse, case or net, and hang in a cool, humid place with gentle airflow, using the temperature, humidity and target weight
loss of a tested recipe. Weigh weekly and record.
- **Case hardening:** outside dries and seals, inside stays wet. Caused by too low
  humidity or too much air movement — raise RH, vacuum-bag for a week to equalise.


## Verify
- [ ] Meat weighed; salt, sugar and cure written down as % and grams.
- [ ] Correct cure type (#1 short/cooked, #2 long/air-dried) dosed to the recipe and the label.
- [ ] Cured refrigerated for the recipe's thickness-based time.
- [ ] Dry-cured pieces reach the recipe's target weight loss with no case hardening.
- [ ] Curing salt stored separately and labelled.

## Checked

Date: 2026-10-25. Jurisdiction: United States (USDA FSIS, 9 CFR 424.21); the rest is general method.

Confirmed in the eCFR text of 9 CFR 424.21(c): sodium or potassium nitrite "shall not result in more than 200 ppm of nitrite, calculated as sodium nitrite in finished product" (bacon excepted under paragraph (b)); chart amount of 1/4 oz sodium nitrite per 100 lb chopped product, which computes to about 156 ppm and matches 0.25 % of a 6.25 % nitrite cure. Removed as unconfirmed: salt and sugar ranges, cure times, brine strengths, injection rate, curing-salt #2 composition, fish freezing figures, air-drying conditions and weight-loss target, mould notes. Bacon-specific limits in paragraph (b) were not read.

Method: documentation only; no commands were run.
