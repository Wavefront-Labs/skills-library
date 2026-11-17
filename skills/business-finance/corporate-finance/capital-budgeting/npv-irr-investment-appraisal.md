---
id: business-finance.corporate-finance.capital-budgeting.npv-irr-investment-appraisal
name: npv-irr-investment-appraisal
category: business-finance
field: corporate-finance
product: capital-budgeting
tags: [capital-budgeting, investment-appraisal, npv, net-present-value, irr, internal-rate-of-return, mirr, payback-period, discounted-payback, profitability-index, hurdle-rate, wacc, cost-of-capital, incremental-cash-flows, sunk-costs, opportunity-cost, terminal-value, sensitivity-analysis, capex, business-case, post-investment-review, xnpv, xirr]
level: practitioner
status: verified
description: "Appraise a capital project properly: incremental after-tax cash flows, the right hurdle rate, NPV first, IRR and payback as context, sensitivities and a post-investment review."
sources: ["https://support.microsoft.com/en-us/office/npv-function-8672cb67-2576-4d07-b67b-ac28acf2a568", "https://support.microsoft.com/en-us/office/xnpv-function-1b42bbf6-370f-4532-a0eb-d67c16b664b7"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPV / IRR investment appraisal

**Goal:** decide whether a project creates value, using cash flows that only include
what changes because of the decision, discounted at a rate that reflects its risk.

## 1. Build incremental, after-tax cash flows
Include only cash flows that differ **with vs without** the project:
- Initial capex (including installation, commissioning, training).
- Incremental revenue and operating costs (not allocated overheads that exist anyway).
- **Working capital** invested at the start and recovered at the end.
- **Tax**: on incremental operating profit, plus the tax shield from depreciation /
  capital allowances (depreciation itself isn't cash).
- **Opportunity costs** (the warehouse you'd otherwise rent out) — include.
- **Sunk costs** (feasibility study already paid) — exclude.
- **Cannibalisation** of existing products — include the lost margin.
- Residual / salvage value net of tax, or a terminal value for long-lived projects.
- **Financing costs (interest) are excluded** — they're in the discount rate.

Keep nominal cash flows with a nominal rate, or real with real; never mix.

## 2. The discount rate
Start from the company **WACC** and adjust for the project's risk: a project
riskier than the average business (new market, new technology) deserves a higher
rate; a cost-saving replacement project may deserve less. Many companies publish
**hurdle rates** by project type. Don't add arbitrary premiums *and* haircut the cash
flows for the same risk.

## 3. Decision metrics
- **NPV** = Σ CFt / (1+r)^t − initial investment. Accept if > 0. Primary metric:
  it measures value in currency and adds across projects.
  Excel: `=NPV(rate, CF1:CFn) + CF0` — Microsoft documents that `NPV()` discounts from one period before
  the first value, so add a time-0 flow outside the function. `XNPV`/`XIRR` take explicit dates (365-day year) and
  treat the first date as the start of the schedule.
- **IRR**: the rate at which NPV = 0. Intuitive but flawed: multiple IRRs when cash
  flows change sign more than once, and it ranks mutually exclusive projects wrongly
  when they differ in size or timing. **MIRR** fixes the reinvestment assumption.
- **Payback / discounted payback**: liquidity and risk signal; ignores everything after
  the payback date. Never the deciding metric alone.
- **Profitability index** (PV of inflows / investment): useful when capital is rationed.

## 4. Stress it
- **Sensitivity:** flex each key driver ±10–20% and show NPV; a tornado chart shows
  which ones matter.
- **Break-even:** the volume, price or cost at which NPV = 0. "Volume can fall 23%
  before NPV is zero" is more useful than a single NPV.
- **Scenarios:** coherent downside/base/upside sets, not every input at its worst.
- Consider **real options** qualitatively: the ability to expand, delay or abandon
  has value a static NPV misses.

## 5. After approval
Set measurable success criteria in the business case (capex, go-live date, run-rate
savings). Run a **post-investment review** at 12–24 months: actual vs case, and why.
Feed systematic optimism back into future approvals.

## Gotchas
- Projects that "always" show IRR just above the hurdle: check for optimistic terminal
  values; state what share of NPV the terminal value supplies.
- Ignoring the working-capital outflow flatters early years.
- Comparing projects with different lives by NPV alone — use equivalent annual
  annuity.
- Using the company's average WACC for a radically different risk profile.

## Verify
- [ ] Cash flows are incremental, after tax, exclude sunk and financing costs.
- [ ] Discount rate basis documented and consistent (nominal/real).
- [ ] NPV computed with the time-0 flow handled correctly.
- [ ] Sensitivity, break-even and scenarios shown; terminal value share stated.
- [ ] Success metrics and a post-investment review date are in the approval.
