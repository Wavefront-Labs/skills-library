---
id: sales-marketing.technical-b2b-sales.solution-selling.building-a-roi-business-case
name: building-a-roi-business-case
category: sales-marketing
field: technical-b2b-sales
product: solution-selling
tags: [solution-selling, value-selling, b2b-sales, enterprise-sales, saas-sales, business-case, roi, roi-calculator, tco, total-cost-of-ownership, payback-period, npv, value-proposition, cost-of-inaction, competitive-positioning, competitive-displacement, executive-summary, cfo, economic-buyer, spreadsheet, value-hypothesis]
level: practitioner
status: draft
description: "Turn technical capability into a buyer-owned business case: value hypothesis, ROI/TCO/payback model in a spreadsheet, conservative assumptions, competitive framing and a one-page exec summary."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building an ROI business case

**Goal:** a business case the buyer's finance team believes because the inputs are
*their* numbers, the assumptions are conservative, and the logic fits on one page.

## 1. From feature to value (the chain)
For each capability write: **Capability → Operational change → Business outcome → Metric.**
Example: "Automated reconciliation → analysts stop matching records by hand → close the
books 3 days faster, fewer errors → hours saved, late-fee/penalty avoided."
Drop any capability you can't take to a metric — it's a feature, not value, for this buyer.

## 2. Gather inputs from discovery
You need the buyer's baseline: volumes, hours, headcount, error rates, current tool costs,
downtime, revenue per unit. Ask for them explicitly ("What does an hour of downtime cost
you?") and note the source next to each number. Inputs you estimate yourself are labelled
`ASSUMPTION` and kept to a minimum.

## 3. The model (one spreadsheet, three tabs)
**Inputs tab** — one cell per input, with source column. **Calc tab** — formulas only.
**Summary tab** — the outputs.
Core formulas (spreadsheet syntax):
```
Annual benefit     = hours_saved_per_week * people * loaded_hourly_cost * 52
                   + errors_avoided_per_year * cost_per_error
                   + other_quantified_gains
Annual cost        = subscription + implementation/3 (if amortised over 3 years) + internal_admin_cost
ROI (yr 1)         = (benefit_y1 - cost_y1) / cost_y1
Payback (months)   = total_upfront_cost / (monthly_benefit - monthly_running_cost)
3-yr NPV           = NPV(discount_rate, net_y1, net_y2, net_y3) - upfront_cost
```
Ask finance what discount rate they use; if they won't say, show undiscounted figures
and say so (rather than inventing a rate).
- **Ramp**: benefits don't start day one — model e.g. 25% / 75% / 100% realisation in
  quarters 1–3 after go-live.
- **Three scenarios**: conservative / expected / optimistic. Lead with conservative.
- **TCO**: include the buyer's internal costs (integration time, training, change
  management). Leaving them out is the quickest way to lose credibility with a CFO.

## 4. Cost of inaction
Show what staying put costs per month — it reframes "is it worth it?" into "can we afford
to wait?". Base it on the same benefit figures.

## 5. Competitive positioning (inside the case, not as a slide war)
- Map the buyer's decision criteria against options: you, competitor, build-in-house, do nothing.
- Win on criteria you're strong at *and* they ranked high; neutralise where you're weak
  with facts, not attacks. "Set traps": ask the buyer to evaluate a criterion where you
  differ, e.g. time to integrate with their ERP.

## 6. Package it
- **One-page executive summary**: problem in their words, recommended solution, conservative
  ROI, payback, cost of inaction, key risks and mitigations, the decision needed and by when.
- Appendix: the spreadsheet, assumptions list, reference customers.
- **Co-author it** with your champion: they present it internally; they must be able to
  defend every number. Send the editable spreadsheet, not a locked PDF.

## Gotchas
- 1000% ROI claims kill credibility — if the number looks too good, cut assumptions.
- Double counting: time saved and headcount reduction for the same hours.
- Counting "soft" benefits (morale, agility) in the total; list them separately.
- Currency and tax: use the buyer's currency; ask whether figures should be pre-tax.

## Verify
- [ ] Every input has a source; assumptions are labelled and few.
- [ ] Conservative scenario still shows payback inside the buyer's usual hurdle (ask for it).
- [ ] Buyer internal costs are included in TCO.
- [ ] Champion has reviewed the model and can explain it unaided.
- [ ] Executive summary fits on one page and names the decision and date.
