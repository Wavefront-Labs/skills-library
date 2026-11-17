---
id: engineering-technology.chemical-engineering.process-design.operating-cost-build-up
name: operating-cost-build-up
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-profitability-analysis, operating-cost-build-up, operating-cost, cost-of-manufacture, raw-material-cost, utility-cost, labor-cost, maintenance-cost, fixed-costs, opex]
level: practitioner
status: draft
description: "Build annual operating cost from raw materials, utilities, labour, maintenance, overheads and fixed charges, with unit consumption factors and cost of manufacture."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operating cost build-up

**Goal:** an annual cost of manufacture and a unit cost per tonne of product.

## Elements
1. **Raw materials**: stream tables give kg per hour; multiply by on-stream hours and the delivered price.
2. **Utilities**: steam, cooling water, electricity, fuel, nitrogen, from duties; use site prices. Compute marginal and average prices where the choice matters.
3. **Operating labour**: operators per shift times the number of shifts crews (a continuous 24-hour plant needs about 4.5 to 5 operators per shift position); apply loaded wage.
4. **Supervision and support**: percentage of operating labour (about 10 to 25% for supervision and clerical in standard texts; confirm).
5. **Maintenance**: percentage of fixed capital per year (about 3 to 6% is typical in textbooks; plant-specific).
6. **Operating supplies, laboratory, royalties and catalyst/chemicals replacement.**
7. **Fixed charges**: insurance, property tax (percentage of capital), depreciation (separate in cash flow).
8. **Overheads**: plant overhead as a percentage of labour and maintenance; general expenses (administration, distribution and selling, research).

## Procedure
1. List consumption per tonne of product from the balance sheet.
2. Price each; keep price basis year and currency.
3. Add by-product credits (revenue) as negative cost.
4. Present cost per tonne with fixed versus variable split.

## Gotchas
- Using electricity price at retail rather than contract rate.
- Forgetting catalyst and solvent make-up.
- Including depreciation twice (in cost of manufacture and in cash flow).

## Verify
- [ ] Unit costs reconcile with the balance sheet.
- [ ] Variable and fixed split clear; breakeven rate computed.
