---
id: transportation-logistics.logistics-supply-chain.supply-chain-planning.forecast-to-sop-cycle
name: forecast-to-sop-cycle
category: transportation-logistics
field: logistics-supply-chain
product: supply-chain-planning
tags: [supply-chain-planning, logistics-supply-chain, demand-forecasting, s-and-op, sop, sales-and-operations-planning, ibp, demand-planning, supply-planning, capacity-planning, safety-stock, forecast-accuracy, mape, wmape, forecast-bias, abc-analysis, xyz-analysis, consensus-forecast, rough-cut-capacity, service-level, excel, python, kinaxis, o9, sap-ibp]
level: practitioner
status: draft
description: "Run a monthly forecast-to-S&OP cycle: baseline statistical forecast, measure WMAPE and bias, consensus review, supply/capacity balance, safety stock from service level, exec sign-off."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forecast to S&OP — a monthly planning cycle that actually closes

**Goal:** turn history and market input into one agreed demand number, check you can
supply it, set inventory targets, and get a decision from leadership — every month,
on a fixed calendar.

## 1. The calendar (typical 5-step monthly S&OP)
| Week | Step | Output |
|---|---|---|
| 1 | Data gathering | Actuals loaded, last month's forecast frozen for accuracy |
| 1–2 | Demand review | Consensus unconstrained forecast, 18–24 month horizon |
| 2–3 | Supply review | Constrained supply plan, capacity gaps flagged |
| 3 | Pre-S&OP / reconciliation | Scenarios with cost and service impact |
| 4 | Executive S&OP | Decisions recorded, plan of record published |
Hold it on the same working days every month; a cycle that slips becomes optional.

## 2. Build the baseline forecast
1. Clean history: remove one-offs (a lost-order spike, stock-outs that suppressed
   sales — use orders or estimated lost demand, not shipments, where you can).
2. Segment SKUs: **ABC** by volume/value, **XYZ** by variability (coefficient of
   variation). AX items get careful models and review; CZ items get simple rules.
3. Fit simple models first: moving average, exponential smoothing (Holt-Winters for
   trend + seasonality). In Python: `statsmodels.tsa.holtwinters.ExponentialSmoothing`.
   Fancier models rarely beat good smoothing on noisy SKU data without strong drivers.
4. Forecast at the level you can predict (family/region), then disaggregate to SKU/DC
   by recent mix.

## 3. Measure it honestly
- **WMAPE** = Σ|actual − forecast| / Σ actual, at the lag that matters (the lead time
  at which you commit supply, e.g. lag 2 months).
- **Bias** = Σ(forecast − actual) / Σ actual. Persistent positive bias = inventory
  build; negative = stock-outs. Bias is usually the more fixable problem.
- **Forecast value added (FVA):** compare naive → statistical → consensus. If sales
  overrides make accuracy worse, show it and stop the override habit.

## 4. Supply and capacity balance
- Convert demand to load on constraints: production lines (hours), suppliers, DC
  throughput, transport capacity.
- Rough-cut check per month: required vs available; flag >90% utilisation as risk.
- Options for gaps: pre-build, overtime, alternate source, allocate scarce supply by
  customer priority, or shape demand (pricing, promotion timing).

## 5. Safety stock
Standard formula when demand varies and lead time is fixed:
`SS = z × σ_d × √L`, with `σ_d` the standard deviation of forecast error per period
(not of demand), `L` lead time in the same periods, `z` from target cycle service level
(90% → 1.28, 95% → 1.65, 98% → 2.05, 99% → 2.33). Add lead-time variability with
`SS = z × √(L·σ_d² + d²·σ_L²)`. Recompute quarterly.

## 6. The executive meeting
Bring decisions, not data: 3–5 issues, each with options, cost, service impact and a
recommendation. Record decisions and owners; the published plan is the single number
for finance, production and logistics.

## Gotchas
- Using shipment history after stock-outs teaches the model that demand was low.
- Measuring accuracy at lag 0 flatters everyone and hides the problem.
- σ of demand instead of σ of forecast error overstates safety stock for predictable items.
- Promotions and new products need a separate overlay process, not the baseline model.
- Too many SKUs reviewed by hand: review by exception (largest error × value).

## Verify
- [ ] Calendar published for 12 months; every step has an owner.
- [ ] WMAPE and bias tracked by family at the committed lag, trending month on month.
- [ ] FVA shows each human step adds accuracy or is removed.
- [ ] Capacity gaps appear in the pre-S&OP pack with costed options.
- [ ] Safety stocks recalculated from current error and lead time.

*Uncertainty:* z-values assume normally distributed error; for intermittent demand
(many zeros) use Croston-type methods and simulation instead.
