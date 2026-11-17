---
id: hospitality-culinary.culinary-arts.menu-engineering.menu-item-mix-analysis-and-repricing
name: menu-item-mix-analysis-and-repricing
category: hospitality-culinary
field: culinary-arts
product: menu-engineering
tags: [menu-engineering, menu-analysis, menu-mix, item-mix, kasavana-smith, stars-plowhorses-puzzles-dogs, stars-and-dogs, contribution-margin, gross-profit, food-cost-percentage, popularity-index, pos-data, menu-pricing, price-anchoring, decoy-pricing, menu-layout, golden-triangle, menu-psychology, seasonal-menu, menu-design, restaurant-profitability, spreadsheet]
level: practitioner
status: draft
description: "Classify every dish as star, plowhorse, puzzle or dog from POS sales and contribution margin, then reprice, rework, reposition or cut — and check the next period moved."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Menu item-mix analysis and repricing

**Goal:** use real sales and costs to decide what to keep, push, rework or drop, so the
menu earns more cash per cover and the kitchen isn't carrying dead items.

## 1. Gather the data (one menu period, same section)
For each item in one **category** (mains with mains, starters with starters):
- **Number sold** in the period, from the POS item report.
- **Selling price** net of tax (VAT/sales tax).
- **Plate cost** from a costed recipe (see
  hospitality-culinary.culinary-arts.recipe-development-and-costing).
Use at least 4 weeks to smooth out daily noise; exclude comped items and specials.

## 2. Calculate (spreadsheet)
| Column | Formula |
|---|---|
| Contribution margin (CM) | price − plate cost |
| Total CM | CM × number sold |
| Menu mix % | item sold ÷ total sold in category |
| Average CM | total CM of category ÷ total sold |
| Popularity threshold | (1 ÷ number of items) × **70 %** |

The 70 % rule comes from the Kasavana–Smith method (1982): an item is "popular" if its
mix % ≥ 70 % of an equal share. With 10 mains, threshold = 10 % × 0.7 = 7 %.

## 3. Classify
| | CM ≥ average | CM < average |
|---|---|---|
| **Mix ≥ threshold** | **Star** | **Plowhorse** |
| **Mix < threshold** | **Puzzle** | **Dog** |

**Food-cost % alone misleads:** a steak at 38 % food cost may earn far more cash per
plate than a pasta at 18 %. Menu engineering ranks by cash margin, not percentage.

## 4. Act on each class
- **Stars** (popular, profitable): protect. Keep the spec tight, best placement, consider
  a small price increase — demand is proven.
- **Plowhorses** (popular, low margin): reduce cost without the guest noticing (portion
  of the expensive component, cheaper garnish, better yield), modest price rise, or
  pair with a high-margin side. Don't remove — they bring people in.
- **Puzzles** (profitable, unpopular): work out why. Rename/redescribe, move to a
  better position, server recommendation, photograph, lower the price slightly.
- **Dogs** (neither): remove or rework entirely, unless it's a deliberate anchor (e.g.
  a vegan option or a signature the brand needs). Each dog costs prep, inventory and
  waste.

## 5. Layout and pricing psychology
These effects are widely taught but evidence for some is mixed — treat as hypotheses
to test, not laws:
- **Eye position:** first item and last item in a list sell better; the "golden
  triangle" eye-scan claim is disputed, but top-of-section placement is consistently
  useful.
- **Box or highlight** one or two stars/puzzles per section, not more.
- **Drop currency symbols and trailing zeros** ("24" not "£24.00"); avoid price columns
  aligned down the right edge that invite comparing on price.
- **Anchor/decoy:** a high-priced item makes the next one down look reasonable.
- **Descriptions:** origin, technique and sensory words lift sales; keep them short.
- Fewer items per section (roughly 5–8) speeds decisions and the kitchen.

## 6. Close the loop
Change only a few things at a time, run another 4-week period, and re-run the matrix.
Compare total CM per cover, not just individual items.

## Gotchas
- Out-of-date plate costs make the whole analysis wrong — re-cost when supplier prices
  move.
- Seasonal items in a short window can look like dogs; compare like with like.
- Items that drive other sales (shared plates, kids' meals) may justify themselves
  indirectly.
- Price rises > ~5–10 % on a star can tip it into a puzzle; step gradually.

## Verify
- [ ] Each category analysed separately with ≥ 4 weeks of POS data.
- [ ] Plate costs dated within the last quarter (or after the last supplier change).
- [ ] Every item has a class and a written action.
- [ ] Follow-up period shows total CM per cover up, or the change is reverted.
