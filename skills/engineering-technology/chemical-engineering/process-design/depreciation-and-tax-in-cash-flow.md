---
id: engineering-technology.chemical-engineering.process-design.depreciation-and-tax-in-cash-flow
name: depreciation-and-tax-in-cash-flow
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-profitability-analysis, depreciation-and-tax-in-cash-flow, depreciation, macrs, straight-line-depreciation, income-tax, tax-shield, after-tax-cash-flow, capital-allowances, cash-flow]
level: practitioner
status: verified
description: "Model depreciation (straight-line, declining balance, tax-schedule methods) and income tax in project cash flow, and state which tax rules were assumed."
sources:
  - "IRS Publication 946, How To Depreciate Property, https://www.irs.gov/publications/p946"
  - "UK government, Work out capital allowances, https://www.gov.uk/work-out-capital-allowances"
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Depreciation and tax in cash flow

**Goal:** after-tax cash flow with the depreciation tax shield, with jurisdiction and rules stated.

## Methods
- **Straight line**: D = (C - S)/n each year.
- **Declining balance / double declining**: D_t = rate x book value at start of year (rate = 2/n for double declining), usually switched to straight-line when it gives larger deduction.
- **Tax schedules** (for example the US MACRS tables, UK capital allowances): fixed percentage by year by asset class. US MACRS uses 200% declining balance for 3-, 5-, 7- and 10-year property and 150% for 15- and 20-year property, switches to straight line when that gives an equal or greater deduction, and defaults to the half-year convention (IRS Publication 946; a 5-year class gives 40% declining balance rate and 20, 32, 19.2, 11.52, 11.52, 5.76% by year, recomputed here). These rules change; use the current rules of your jurisdiction and confirm with a tax adviser.

## In the cash flow
1. Taxable income = revenue - cash operating cost - depreciation (and interest, if levered).
2. Tax = rate x taxable income (zero if negative, or carry losses forward per local rules).
3. Cash flow = revenue - cash costs - tax - capital (depreciation is not a cash flow; it only changes tax).

## Procedure
1. Allocate capital to asset classes with different depreciation lives.
2. Apply the schedule to each class; sum by year.
3. Compute tax with the effective rate (combine national and local rates, and state it).
4. Compare NPV with and without accelerated schedule to see the value of the shield.

## Gotchas
- Mixing book depreciation (accounting) and tax depreciation.
- Forgetting that start-up costs and working capital may be treated differently for tax; check the local rules.
- Applying a historical tax rate to a project that will run for 20 years without stating the assumption.

## Verify
- [ ] Sum of depreciation over life equals depreciable base.
- [ ] Tax assumptions written next to the model with the date they were checked.
