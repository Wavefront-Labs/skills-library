---
id: hospitality-culinary.bartending.bar-inventory-and-costing.stocktake-pars-and-pour-cost-variance
name: stocktake-pars-and-pour-cost-variance
category: hospitality-culinary
field: bartending
product: bar-inventory-and-costing
tags: [bar-inventory-and-costing, bar-inventory, stocktake, stock-count, par-levels, ordering, pour-cost, beverage-cost, cost-of-goods, cogs, variance, shrinkage, over-pouring, spillage, comps, wastage-log, bottle-weighing, tenths, keg-yield, supplier-management, beverage-management, bar-manager]
level: practitioner
status: draft
description: "Control bar stock: set par levels and order to them, run a consistent stocktake (tenths or weighing), calculate pour cost, find variance against POS sales, and trace shrinkage causes."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stocktake, pars and pour-cost variance

**Goal:** know what the bar *should* have used against what it *did* use, and close the
gap. Every percentage point of pour cost on a busy bar is real money.

## 1. Par levels and ordering
- **Par** = the quantity you want on hand after delivery to cover usage until the
  next delivery, plus a safety buffer.
  `par ≈ (average usage per day × days between deliveries) + safety stock`
- **Order quantity = par − on hand** (rounded to case sizes where sensible).
- Review pars monthly and seasonally; events and menu changes shift usage.
- Keep slow movers lean; dead stock is cash on a shelf.

## 2. Stocktake routine
- Same day, same time, same order (shelf to shelf, left to right), ideally before
  opening or after close when nothing moves.
- **Partials**: estimate in **tenths** of a bottle by eye, or **weigh** open bottles on
  a scale (weight − empty bottle weight, ÷ liquid density ≈ volume). Weighing is more
  accurate; many inventory apps do the maths with stored tare weights.
  *[App accuracy depends on maintained tare/density data.]*
- **Kegs**: weigh or use flow meters; foam, line cleaning and fobbing mean real keg
  yield is lower than nominal — track your own.
- Two people for count + entry where possible; count storage and the bar.

## 3. Calculating usage and pour cost
`usage (cost) = opening stock + purchases − closing stock` (all at cost)
`pour cost % = usage ÷ beverage sales (net of tax)`
Example: opening $8,000 + purchases $5,000 − closing $7,500 = $5,500 used; sales
$25,000 → **22%**. Compare by category (spirits, beer, wine, cocktails) — a blended
number hides problems.

## 4. Variance: the real control
Variance compares **theoretical usage** (from POS sales × recipe specs) to **actual
usage** (from the count):
1. Export POS item sales for the period.
2. Multiply by each recipe's pour (e.g. 120 Margaritas × 50 ml tequila = 6 L).
3. Compare to the counted usage per product (tequila actually used: 6.9 L).
4. Variance = actual − theoretical (here 0.9 L, ~15% over).
Investigate any product over a set tolerance (many bars use ~2–5%).

## 5. Common causes of shrinkage
| Signal | Likely cause |
|---|---|
| One spirit consistently over | Over-pouring / free-pouring that spirit; unrung drinks |
| Draught beer high variance | Foam waste, line cleaning not logged, bad pours, unrung pints |
| Wine by the glass over | Oversized pours, open bottles spoiling |
| Everything slightly over | Spillage, comps/staff drinks not recorded |
| Premium bottle short, wells fine | Theft or substitution |
| Counts swing wildly | Inconsistent counting method |
Fixes: jiggers everywhere, every drink rung in, a **wastage/comp log** (spills, remakes,
comps, staff drinks), correct glassware, spot-checks of pours, keys/locks for back
stock.

## 6. Supplier management
Check deliveries against the invoice and order: product, size, count, and price (price
creep hides here). Record credits for breakages. Get best prices on high-volume SKUs;
watch minimum-order traps.

## Gotchas
- Counting in different units (bottles vs ml) across weeks.
- Forgetting product transferred to the kitchen (wine for cooking) — record transfers.
- Using invoice-date vs delivery-date purchases inconsistently.
- POS buttons that don't match real recipes (e.g. a "double" button that rings single).

## Verify
- [ ] Stocktake done on schedule with the same method each time.
- [ ] Pour cost calculated by category, compared to target.
- [ ] Variance report run; every product over tolerance has a noted cause and action.
- [ ] Wastage/comp log reconciles to the variance.
