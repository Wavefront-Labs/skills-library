---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.machine-ownership-cost-estimation
name: machine-ownership-cost-estimation
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, ownership-cost, machinery-management, depreciation, machinery-cost, fixed-cost, interest-on-investment]
level: practitioner
status: draft
description: "Estimate annual fixed ownership cost for a farm machine: depreciation, interest, taxes, housing and insurance, and put it on a per-hour and per-hectare basis."
sources:
  - "Hunt & Wilson, Farm Power and Machinery Management"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Machine ownership cost

**Goal:** a defensible fixed cost per year, per hour and per hectare, for budgeting or own-versus-hire decisions.

## Components (annual)
1. **Depreciation** - `(P - S) / n` for straight line (P purchase price, S salvage, n years), or use the remaining-value curve for the machine type. ASABE D497 publishes remaining-value (percent of list price by age and annual use) coefficients per machine class; take the coefficients from the current standard, do not rely on remembered figures.
2. **Interest on investment** - `i x (P + S) / 2` using the average investment. Use the farm's opportunity cost of capital or borrowing rate.
3. **Taxes, housing, insurance (THI)** - a percentage of purchase price per year. Rules of thumb in textbooks are about 1 percent for housing, 0.25-1 percent for insurance and local-rate taxes; replace with actual local figures.

## Convert to unit costs
- `cost per hour = annual ownership cost / annual hours`
- `cost per ha = cost per hour / effective field capacity (ha/h)` (see the field-efficiency skill).
- Break-even hours versus custom hire: `ownership cost / (hire rate per h - operating cost per h)`.

## Gotchas
- Use real expected annual hours; low-use machines are dominated by fixed cost.
- Do not include operator labour, fuel or repairs here; those are operating costs.
- Inflation: do the whole calculation in real or nominal terms, not mixed.
- Tax treatment (depreciation allowances) is jurisdiction-specific; this is an engineering cost, not tax advice.

## Verify
- [ ] Salvage value matches a published remaining-value curve or dealer quotes for the same age and hours.
- [ ] Annual hours are from logs or a credible plan.
- [ ] Unit cost times annual output reproduces the annual total.
