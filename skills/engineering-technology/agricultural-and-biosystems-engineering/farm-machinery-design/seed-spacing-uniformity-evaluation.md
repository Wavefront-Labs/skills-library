---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.seed-spacing-uniformity-evaluation
name: seed-spacing-uniformity-evaluation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, seed-spacing-uniformity, planter-design, quality-of-feed-index, singulation, plant-spacing-cv, emergence-uniformity]
level: practitioner
status: draft
description: "Measure and score planter seed spacing: skips, multiples, quality-of-feed index and coefficient of variation, with how to dig or stand-test and interpret results."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Seed spacing uniformity evaluation

**Goal:** quantify planter accuracy and find which row units or settings are failing.

## Measures
Let `x` be the target spacing. Classify each measured spacing:
- **Multiples**: spacing < 0.5 x.
- **Skips (misses)**: spacing > 1.5 x.
- **Acceptable**: 0.5 x to 1.5 x. The percentage acceptable is the *quality of feed index* (Kachman and Smith approach); higher is better.
- **Precision**: coefficient of variation of the acceptable spacings (not including skips and multiples).

Standards for the lab test method exist for precision planters (ISO 7256-1 covers single-seed drills test methods; check the current edition).

## How to measure
1. **Test stand or sticky belt**: run the meter at working speed over a grease or adhesive belt; mark seed positions and measure.
2. **Field**: dig up seedlings or stake rows after emergence (record at least 100-200 plants per row); measure plant spacing.
3. Compute proportions and CV for each row unit; compare to others.

## Interpreting
Skips from low vacuum or worn meters; multiples from high vacuum or poor singulator; poor spacing at higher speed often indicates bounce in the seed tube; rough fields cause erratic ground contact.

## Gotchas
- Field emergence differs from seed spacing due to seed depth and soil conditions.
- Row-to-row variability in down force can cause both depth and spacing errors.

## Verify
- [ ] Sample size is large enough to produce stable percentages.
- [ ] Spacing reported with target and speed.
