---
id: engineering-technology.chemical-engineering.process-design.contingency-and-working-capital
name: contingency-and-working-capital
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-capital-cost-estimation, contingency-and-working-capital, contingency, working-capital, owners-cost, capital-estimate, startup-cost, risk-allowance, total-capital-investment]
level: practitioner
status: draft
description: "Add contingency, owner's cost and working capital to a capital estimate, with methods (percentage, range-based) and what each must cover and not cover."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contingency and working capital

**Goal:** a total capital investment that includes the allowances the project will actually need.

## Contingency
Contingency covers uncertainty in the scope as defined (quantities, prices, productivity), not scope growth (that is a change) and not escalation (a separate item). Methods:
1. **Percentage of base cost** by estimate class: larger at earlier stages (often 20 to 50% at screening level, 10 to 20% at budget level; set your own policy).
2. **Line-item**: percentage per cost element by definition level.
3. **Range analysis (Monte Carlo)**: distributions on major costs; set contingency at a chosen confidence level (for example P50 or P80), state it.

## Other additions
- **Owner's costs**: project team, permits, land, spares, start-up, training.
- **Start-up**: commissioning, initial catalyst and chemicals, lost production in ramp-up.
- **Working capital**: inventory of raw materials, products and spare parts plus accounts receivable minus payable; a first estimate is a number of weeks of cost or a fraction of fixed capital (about 10 to 20% is a typical screening value, confirm for your industry).

## Practice
Show base cost, contingency, escalation and owner's cost as separate lines; the reader can then challenge each.

## Gotchas
- Lumping scope growth into contingency hides governance problems.
- Working capital is recovered at the end of project life; model it as an outflow at start and inflow at end.
- Contingency is not a management reserve.

## Verify
- [ ] Contingency method and percentage recorded with the class.
- [ ] Working capital entered as time-phased cash flows.
