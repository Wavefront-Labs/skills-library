---
id: creative-arts.fashion-design.knitwear-design.yarn-count-systems-nm-ne-denier-tex
name: yarn-count-systems-nm-ne-denier-tex
category: creative-arts
field: fashion-design
product: knitwear-design
tags: [fashion-design, knitwear-design, yarn-count-systems, nm-count, yarn-count, denier, tex, knitwear-yarn]
level: practitioner
status: draft
description: "Read and convert yarn counts: metric Nm, cotton Ne, worsted count, denier, dtex and tex; ply notation like 2/28 Nm, and picking count for a machine gauge."
sources:
  - https://en.wikipedia.org/wiki/Units_of_textile_measurement
  - https://en.wikipedia.org/wiki/Yarn
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Yarn count systems (Nm, Ne, denier, tex)

**Goal:** read yarn tickets correctly, convert between systems, and pick the count that suits
a machine gauge.

## Two families
- **Indirect (length per weight; higher = finer):** Nm, Ne, worsted (NeK).
- **Direct (weight per length; higher = thicker):** tex, dtex, denier.

| System | Definition |
|---|---|
| **Nm** (metric) | km per kg (m per g). 1/28 Nm = 28,000 m per kg |
| **Ne** (English cotton) | number of 840-yard hanks per lb |
| **Worsted (NeK)** | number of 560-yard hanks per lb |
| **tex** | grams per 1000 m |
| **dtex** | grams per 10,000 m |
| **denier** | grams per 9000 m |

## Conversions
- tex = 1000 / Nm; Nm = 1.693 x Ne; denier = 9 x tex = 9000 / Nm; dtex = 10 x tex.
- Example: 2/28 Nm = two ends of 28 Nm plied = resultant 14 Nm (about 71 tex).

## Ply notation
- Knitwear convention is **plies/count**: 2/28 Nm = 2 singles of Nm 28. Cotton often writes
  count/plies: 30/1 Ne.
- Resultant count = single count / number of plies (for same-count singles).

## Count to gauge (rough guide for wool on flat machines, total resultant Nm)
| Gauge | Resultant Nm |
|---|---|
| 3-5 gg | 2.5-5 |
| 7 gg | 5-8 |
| 12 gg | 12-16 |
| 14-16 gg | 16-24 |
| 18 gg | 24-30 |

## Gotchas
- Mixing direct and indirect systems in a spec sheet is a common error.
- Fancy yarns (bouclé, chenille) behave thicker than their count.
- Elastane is always quoted in denier/dtex.

## Verify
- [ ] Count and system stated on every yarn line of the spec.
- [ ] Resultant count suits the gauge (swatch confirms).
