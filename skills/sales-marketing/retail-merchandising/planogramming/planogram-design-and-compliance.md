---
id: sales-marketing.retail-merchandising.planogramming.planogram-design-and-compliance
name: planogram-design-and-compliance
category: sales-marketing
field: retail-merchandising
product: planogramming
tags: [planogramming, planogram, pog, retail-merchandising, shelf-layout, facings, days-of-supply, space-to-sales, space-allocation, eye-level, vertical-blocking, horizontal-blocking, category-management, compliance-audit, shelf-reset, gondola, shelf-ready-packaging, grocery, fmcg, cpg]
level: practitioner
status: draft
description: "Design a planogram that earns its space: allocate facings by sales and days of supply, block and position by shopper logic, then audit store compliance and fix gaps."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Planogram design and compliance — engineering the shelf

**Goal:** every item gets space in proportion to what it earns, the shelf reads the way the
shopper decides, nothing runs out between deliveries, and stores actually build it.

## 1. Gather the inputs (per store cluster)
- **Item list** with dimensions (W×H×D), case pack, and whether it's shelf-ready packaging.
- **Sales:** units/week and gross margin £/$ per week, ideally 13–52 weeks to smooth seasonality.
- **Fixture:** bay width (common gondola bays are 1.0 m / 4 ft; confirm yours), shelf
  count, shelf depth, notch pitch.
- **Replenishment:** delivery frequency and shelf-fill frequency.
- **Rules:** must-stock items, supplier agreements (paid placement), adjacencies.

## 2. Allocate facings — the core arithmetic
Units on shelf for an item = facings × units deep × units high.
Target **days of supply (DOS)** on shelf = units on shelf ÷ (units/week ÷ trading days).
- Set a minimum DOS that covers the gap between deliveries plus safety: e.g. delivered
  every 2 days, aim ≥ 3–4 DOS on shelf; also at least **1 case pack + some** so a full
  case fits at fill time (otherwise backroom stock piles up).
- Start with **space share ≈ sales share** (units for availability; margin or a blend
  for profit focus). In a spreadsheet:
  ```
  space_share  = item_sales / category_sales
  target_width = space_share * total_shelf_cm
  facings      = max(1, ROUND(target_width / item_width_cm))
  dos          = (facings * deep * high) / (weekly_units / 7)
  ```
  Then adjust: raise facings where DOS < minimum, cut where DOS is far above (e.g. >14
  days) — that space is better used elsewhere.
- Delist candidates: bottom-ranked items by sales and margin that aren't must-stock or
  the only option for a need (check with the category manager — "unique" items keep shoppers).

## 3. Position by how the shopper chooses
- **Block** by the shopper's first decision (the "decision tree"): e.g. coffee → format
  (beans/ground/pods) → brand → size. Don't guess; use loyalty-card switching data or
  ask category management.
- **Vertical blocking** (a brand or segment as a column across shelves) helps scanning
  along the aisle; horizontal blocking suits small items or price tiers.
- **Eye level to chest level** is prime: put high-sellers and high-margin there; heavy and
  bulky on the bottom; kids' items lower. Place the category leader mid-aisle to draw
  shoppers past the rest, not at the entry end.
- **Price ladder:** own-label next to the brand leader, typically to its right.

## 4. Publish and audit compliance
- Issue a planogram PDF with a shelf-by-shelf item list, positions numbered left to right,
  shelf heights, and shelf-edge label order. Version-date it.
- **Audit**: within a week of the reset, check a sample of stores. Score:
  `compliance % = correctly placed facings ÷ planned facings`. Photograph each bay.
  Common target: 90%+ (set your own).
- Log *why* items are out of place: product not delivered, didn't fit (dimensions wrong
  in the data), staff preference, or a gap filled with a neighbour.

## Gotchas
- **Wrong dimensions** in the master data are the #1 cause of planograms that can't be
  built. Measure real packs for new lines.
- **Gap-filling** with a neighbour hides out-of-stocks from reports; train staff to
  leave the gap labelled or follow a substitution rule.
- Space-to-sales ignores **elasticity**: some items sell more with more space, many don't.
  Test before giving a slow item a bigger block.
- One planogram per store is unmanageable; cluster stores by fixture size and demographics
  (often 3–6 versions per category).

## Verify
- [ ] Every item meets the minimum DOS and holds a full case pack.
- [ ] Space share is within a few points of sales (or margin) share for top items.
- [ ] The layout follows a documented customer decision tree.
- [ ] Planogram fits the actual fixture (shelf heights and depths checked).
- [ ] Post-reset compliance audit done with photos; root causes logged.
- [ ] Out-of-stock and sales per metre compared before vs after over 4+ weeks.
