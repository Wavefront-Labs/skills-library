---
id: engineering-technology.chemical-engineering.process-design.discounted-cash-flow-npv-irr
name: discounted-cash-flow-npv-irr
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-profitability-analysis, discounted-cash-flow-npv-irr, npv, irr, discounted-cash-flow, dcf, payback, cash-flow, discount-rate, project-evaluation, profitability]
level: practitioner
status: verified
description: "Evaluate a project with discounted cash flow: build the annual cash flow, compute NPV and IRR, payback and discounted payback, and avoid the common timing mistakes."
sources:
  - "Towler and Sinnott, Chemical Engineering Design; Turton et al., Analysis, Synthesis and Design of Chemical Processes; Peters, Timmerhaus and West, Plant Design and Economics (textbooks, method only)"
  - "Identity (rev - cost - dep)(1 - t) + dep = (rev - cost)(1 - t) + t dep and the IRR example computed with Python"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Discounted cash flow, NPV and IRR

**Goal:** a transparent annual cash-flow model and the decision metrics.

## Cash flow per year
CF_t = (revenue - cash operating cost - depreciation) x (1 - tax rate) + depreciation - capital expenditure - change in working capital
(equivalently, after-tax operating cash plus the depreciation tax shield; use your tax regime's rules, and confirm them).

## Metrics
- **NPV** = sum over t of CF_t / (1 + i)^t, with i the discount rate (hurdle rate). Accept if NPV > 0.
- **IRR**: the discount rate at which NPV = 0. Compare with hurdle rate. Multiple sign changes can give multiple IRRs (for example -100, +230, -132 gives both 10% and 20%, computed).
- **Payback**: years until cumulative undiscounted cash flow becomes positive; **discounted payback** uses discounted flows.
- **Profitability index** = NPV / PV of capital (some texts use PV of inflows / PV of outflows; state which).

## Procedure
1. Time-phase capital (for example 30, 40, 30% over the construction years).
2. Ramp-up production (for example 60 to 80% in the first year).
3. Add working capital outflow at start and recovery at end; add salvage value if any.
4. Compute NPV at the hurdle rate; compute IRR with a spreadsheet function.
5. Test results with `engineering-technology.chemical-engineering.process-design.project-sensitivity-and-risk-analysis`.

## Gotchas
- Mixing nominal cash flows with a real discount rate (or vice versa).
- Treating depreciation as cash cost.
- Ignoring plant life: state the evaluation period and treat terminal value consistently.

## Verify
- [ ] NPV recomputed from a second independent method (spreadsheet NPV versus manual sum) agrees.
- [ ] Timing of capital and revenue shown on a chart.
