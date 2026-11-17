---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.budget-variance
name: budget-variance
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-budgeting, budget-variance, budget-vs-actual, overrun-process, holdback]
level: practitioner
status: docs-checked
description: "Manage budget vs actual variance using the FinOps Budgeting capability: variance thresholds by maturity, overage escalation through holdback, favourable variance."
sources: ["https://www.finops.org/framework/capabilities/budgeting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Budget variance management

## Steps
1. Measure budget against actuals using discount-adjusted, amortised cloud usage data, as the budgeting strategy specifies.
2. Set acceptable variance thresholds for both budget-to-forecast and budget-to-actual. The FinOps
   Framework gives a maximum variance from actual spend of 20% at Crawl, 15% at Walk and 12% at Run.
3. Notify stakeholders when an actual or anticipated variance threshold is exceeded and overspend is at risk.
4. Resolve an overage in escalating steps:
   - The threshold report anticipates exceeding budget (Engineering).
   - Engineering and Product investigate the cause.
   - Either take corrective optimisation action, or ask the budget owner for extra funding from holdback.
   - If that is not enough, involve a higher-level budget owner or Finance, who may designate funding from a higher-level holdback.
   - Finally, involve Leadership to approve the adjustment, or deny it and agree corrective action.
5. Record overrides, exceptions and service impacts.

## Gotchas
- Unfavourable to budget (more spend than planned) needs action as soon as it is detected.
- Strongly favourable to budget is also not ideal: unused holdback could fund other areas, so budget owners and Finance should reclaim holdback that is no longer needed.
- Agree an exception process for out-of-cycle budget changes in advance.

## Verify
- [ ] Variance thresholds are defined for budget-to-forecast and budget-to-actual.
- [ ] Overage decisions (fund from holdback, escalate, deny) are recorded.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Budgeting capability page (full text read).
Removed as unconfirmed: flexed-budget formula, example thresholds (5 percent, 10 percent, 5k), variance classification list, year-to-date tracking and the 2-3 line explanation standard.
