---
id: agriculture-environment.horticulture.market-gardening.crop-plan-and-succession-schedule
name: crop-plan-and-succession-schedule
category: agriculture-environment
field: horticulture
product: market-gardening
tags: [horticulture, market-gardening, market-garden, small-farm, crop-plan, crop-planning, succession-planting, bed-feet, standard-beds, 30-inch-beds, intensive-spacing, days-to-maturity, harvest-window, csa, veg-box, farmers-market, yield-per-bed, revenue-per-bed, transplant-schedule, seeding-schedule, spreadsheet, bio-intensive, no-dig, paperpot, bed-prep, crop-rotation]
level: practitioner
status: draft
description: "Build a market-garden crop plan backwards from sales: weekly demand to bed-feet, harvest windows to sowing dates, succession intervals, and a field map with standard beds and rotation."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crop plan and succession schedule

**Goal:** a spreadsheet that turns "we sell 60 veg boxes and two markets a week" into
exactly what to seed, when, and in how many bed-feet — so the right crops are ready
every week of the season and beds are never idle.

> Draft. Yields and maturity times vary hugely by climate, variety and skill; use the
> numbers below only to start the first year's plan, then replace them with your own
> harvest records.

## 1. Standardise the beds
- Pick one bed size and stick to it: e.g. **75 cm (30 in) wide beds, 45 cm paths,
  15 m or 30 m long**. Every tool (seeder, row cover, irrigation line, net) is sized to it.
- Plan in **bed-feet / bed-metres**, not plants.

## 2. Start from sales
For each crop and week, estimate demand: units/week (bunches, bags, kg, heads).
Example: 60 boxes × 1 head lettuce + 40 heads for market = 100 heads/week for 20 weeks.

## 3. Convert demand to bed-length per succession
Columns per crop:
- **Yield per bed-metre** (e.g. lettuce at 4 rows × 25 cm in-row ≈ 16 heads/bed-m,
  allow 10–20% loss → ~13 saleable).
- **Harvest window** — how many weeks one planting stays saleable (lettuce ~1–2 wk,
  carrots ~3–6 wk in ground, kale many weeks).
- **Bed-m per succession** = weekly demand × weeks covered ÷ yield per bed-m.
  Lettuce: 100/wk × 1.5 wk ÷ 13 ≈ 12 bed-m every ~1.5 weeks, rounded up to whole beds or half-beds.

## 4. Work backwards to seeding dates
- For each target first-harvest date: **transplant date = harvest − days to maturity
  (from transplant)**; **seed date = transplant − days in the propagation house**
  (lettuce ~3–4 weeks, brassicas ~4–6, alliums ~8–10).
- Add a **"fall factor"**: crops maturing as days shorten (late summer onward) take
  ~1–2+ weeks longer — add it to late successions.
- **Succession interval** = harvest window. If one planting is saleable for 2 weeks,
  plant every 2 weeks.
- Last planting: count back from first frost (or end of season) with the fall factor.

## 5. Map it to beds
- Assign each succession to a specific bed and dates (in and out) so you can see turnovers:
  e.g. spring radish (30 days) → early summer lettuce → autumn spinach, in one bed.
- Group crops by family into blocks to rotate (3–4 year cycle) and to share netting/cover
  (brassicas under insect mesh together).
- Check **bed occupancy per week** never exceeds beds available.

## 6. Outputs that run the season
- **Weekly seeding sheet** (crop, variety, trays/cells, date).
- **Weekly transplant/direct-seed sheet** (bed ID, crop, spacing, rows).
- **Harvest forecast** by week to compare against sales.
- Order seed for the plan + ~20–30% spare.

## 7. Record and adjust
Log actual seed dates, transplant dates, first/last harvest and yield per bed. That
becomes next year's maturity and yield columns — the plan improves every season.

## Gotchas
- Plan for crop failures: keep 10–20% overplanting on core crops.
- Over-planting long-season, low-value crops (e.g. maincrop potatoes, winter squash on
  small plots) eats bed space; compare **revenue per bed-metre per week**.
- Bed turnovers fail when prep (clear residue, amend, irrigation reset) isn't scheduled — budget a day.

## Verify
- [ ] Every crop row in the sheet traces: demand → bed-m → seed date → bed ID.
- [ ] Succession intervals equal harvest windows; fall factor added late season.
- [ ] Weekly bed occupancy ≤ beds available.
- [ ] Harvest forecast covers each sales week with ≥ 10% margin on core crops.
- [ ] Actual dates and yields are being logged for next year.
