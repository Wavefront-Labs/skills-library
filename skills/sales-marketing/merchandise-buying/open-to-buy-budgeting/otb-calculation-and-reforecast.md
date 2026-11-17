---
id: sales-marketing.merchandise-buying.open-to-buy-budgeting.otb-calculation-and-reforecast
name: otb-calculation-and-reforecast
category: sales-marketing
field: merchandise-buying
product: open-to-buy-budgeting
tags: [open-to-buy-budgeting, open-to-buy, otb, merchandise-buying, merchandise-planning, wssi, weekly-sales-stock-intake, receipt-flow, intake, stock-to-sales, weeks-of-cover, bom-stock, eom-stock, markdowns, imu, initial-markup, on-order, chase, cancel, reforecast, inventory-planning, retail-math]
level: practitioner
status: draft
description: "Calculate and manage open-to-buy: the OTB formula at retail and cost, monthly receipt flow, weekly reforecasting against sales, and when to chase or cancel orders."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# OTB calculation and reforecast

**Goal:** control the money a buyer may still spend on stock in each period, so
the store is never over-stocked into markdown or starved of best-sellers.
Open-to-buy (OTB) is a living number — recalculated every week as actual sales
diverge from plan.

## 1. The formula (per category, per month)
At retail value:
```
Planned purchases = Planned sales + Planned markdowns (+ shrink allowance)
                    + Planned end-of-month (EOM) stock − Beginning-of-month (BOM) stock
OTB               = Planned purchases − Stock already on order for that month
```
Convert to cost: `OTB at cost = OTB at retail × (1 − IMU%)`, where IMU is the
initial markup as a % of retail.

Worked example: planned sales 100k, markdowns 8k, EOM 220k, BOM 200k, on order
90k → purchases = 100 + 8 + 220 − 200 = 128k; OTB = 128 − 90 = **38k retail**; at
55% IMU → **17.1k at cost**.

## 2. Setting planned stock levels
- Planned EOM usually = next month's BOM, derived from a **stock-to-sales ratio**
  or **weeks of cover** target (e.g. 8 weeks of forward sales for fashion basics,
  less for perishable trend).
- `Weeks of cover = stock ÷ average weekly forward sales`.
- Build it in a **WSSI** (weekly sales, stock and intake) sheet: rows = weeks,
  columns = sales (plan/actual/LY), markdowns, intake (plan/actual/on order),
  closing stock, cover. Most planning systems (or a spreadsheet) do this.

## 3. Receipt flow
Phase intake so stock lands just before demand: launch deliveries 2–4 weeks
ahead of the selling peak; split big buys into 2–3 drops to keep newness and
retain flexibility. Check that supplier lead times allow the phasing.

## 4. Weekly reforecast
1. Load actual sales, markdowns and receipts.
2. Reforecast remaining weeks — e.g. apply the trend in recent weeks vs plan
   (if running at 90% of plan for 4 weeks, reforecast near-term at ~90% unless
   there's a known reason it will recover).
3. Recalculate closing stock and OTB.
4. Flag categories: **overbought** (projected cover above target / OTB negative) and
   **underbought** (cover below target with strong sell-through).

## 5. Chase and cancel calls
- **Chase** (repeat or add) when sell-through is ahead, cover is short and the
  supplier can deliver inside the selling window. Use OTB held in reserve —
  plan to keep ~10–20% of season OTB uncommitted at the start for this (**uncertain:**
  reserve % is a house choice).
- **Cancel/delay** when OTB is negative: in order of least damage — delay deliveries,
  reduce quantities, cancel late-delivering orders (often contractually allowed
  when the supplier misses the ship date), move stock between categories.
- Each decision: record the OTB effect and margin impact.

## Gotchas
- Mixing cost and retail values in one calculation — keep a column convention.
- Ignoring markdowns in planned purchases understates the stock needed to hit EOM.
- On-order data must include *all* open POs, including unconfirmed and consolidated ones.
- Negative OTB is a signal, not a rule to stop buying core replenishment; check by line.

## Verify
- [ ] OTB computed per category/month at retail and cost, with on-order deducted.
- [ ] EOM targets tied to weeks-of-cover or stock-to-sales goals.
- [ ] WSSI updated weekly with actuals and a reforecast.
- [ ] Over/underbought categories flagged with chase/cancel actions.
- [ ] Reserve OTB tracked and used deliberately.
