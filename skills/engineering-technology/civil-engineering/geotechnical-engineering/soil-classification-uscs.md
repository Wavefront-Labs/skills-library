---
id: engineering-technology.civil-engineering.geotechnical-engineering.soil-classification-uscs
name: soil-classification-uscs
category: engineering-technology
field: civil-engineering
product: geotechnical-engineering
tags: [soil-classification, uscs, astm-d2487, atterberg-limits, plasticity-chart, sieve-analysis, aashto-classification, geotechnical]
level: practitioner
status: draft
description: "Classify soil with USCS from sieve and Atterberg results: coarse vs fine split, group symbols, plasticity chart, field checks and common misclassifications."
sources: ["ASTM D2487 Standard Practice for Classification of Soils for Engineering Purposes (USCS)", "ASTM D2488 Description and Identification of Soils (Visual-Manual)", "Das, Principles of Geotechnical Engineering"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Soil classification (USCS) from lab data

**Goal:** a defensible group symbol and name that drives drainage, frost, compaction and strength assumptions.

## Procedure
1. Wash sieve test: percent passing the No. 200 sieve (0.075 mm). Under 50% = coarse-grained; 50% or more = fine-grained.
2. Coarse-grained: gravel (G) if more than half the coarse fraction is retained on the No. 4 sieve (4.75 mm), else sand (S).
3. Fines under 5%: clean, so GW/GP or SW/SP from gradation. Cu = D60/D10 and Cc = D30^2/(D10*D60). Well graded if Cu >= 4 (gravel) or >= 6 (sand) and Cc between 1 and 3.
4. Fines over 12%: GM/GC or SM/SC, decided by whether the Atterberg limits plot below or above the A-line. 5 to 12% gives dual symbols (e.g. SW-SM).
5. Fine-grained: plot LL and PI on the plasticity chart. Above the A-line with LL under 50 is CL; LL 50 or more is CH. Below the A-line is ML or MH (OL/OH if organic: oven-dried LL under 75% of undried LL). The CL-ML zone (PI 4 to 7) takes a dual symbol.
6. A-line: PI = 0.73(LL - 20). Check against the standard before relying on a plot.

## Gotchas
- Visual-manual field description (D2488) gives only a probable symbol; do not report it as D2487.
- Dry-sieving a plastic soil gives wrong fines content: wash it.
- Highway work often uses AASHTO M 145 groups (A-1 to A-7); the two systems are not interchangeable.
- Cobbles and boulders are removed before classification and reported separately.

## Verify
Fines content, LL and PI recorded with test dates; symbol re-derived independently by a second person; logs show symbol and name.

> Professional guidance only. Design, sign-off and site decisions belong to a licensed/chartered engineer applying the codes adopted in the project jurisdiction; check edition and local amendments.
