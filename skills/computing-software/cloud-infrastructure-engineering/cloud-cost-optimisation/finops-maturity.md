---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-maturity
name: finops-maturity
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-principles, finops-maturity, crawl-walk-run, maturity-model, capability-maturity, finops-assessment]
level: practitioner
status: docs-checked
description: "Use the FinOps Crawl/Walk/Run model per capability: level characteristics, community sample goals (allocation, coverage, forecast variance) and how to pick targets."
sources: ["https://www.finops.org/framework/maturity-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FinOps maturity: Crawl, Walk, Run

Maturity is assessed per capability or functional activity, not once for the organisation. Each
can sit at a different level. The labels are general guidelines: the goal is never simply Run
everywhere. Business value should drive the choice, so prioritise maturing the capabilities that give the highest value.

## Level characteristics (FinOps Framework)
- Crawl: very little reporting and tooling; basic KPIs and basic processes and policies; understood but not followed by all major teams; plans address low hanging fruit.
- Walk: understood and followed in the organisation; automation or process covers most requirements; difficult edge cases are identified and either knowingly ignored or estimated; medium to high KPI goals.
- Run: understood and followed by all teams; difficult edge cases are being addressed; very high KPI goals; automation is the preferred approach.

## Sample community goals (data.finops.org, quoted on the Framework page)
| Measure | Crawl | Walk | Run |
|---|---|---|---|
| Cost allocated to a known owner | at least 70% | at least 85% | more than 90% |
| Commitment discount target coverage | about 60% | above 75% | above 80 |
| Forecast to actual accuracy variance | below 20% | below 10% | below 5% |

## Steps
1. Score each capability with its measure and the process characteristics above.
2. Choose a target level per capability from the business value of improving it; stay at Walk where Walk already meets the measure of success.
3. Mature the highest-value capabilities first, taking quick small actions and reviewing their outcomes.

## Gotchas
- Effort spent maturing a capability that already meets its measure of success gives no benefit.
- The FinOps Assessment (see the assessment skills) offers a rubric to communicate the current level.

## Verify
- [ ] Each capability has a measure, a current level and a target level with a reason.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Foundation Maturity Model page (full text read). The capabilities index page was a navigation page only and is no longer cited.
Removed as unconfirmed: the table rows for anomaly management and reporting, the 15 percent and 12 percent forecast markers, the 50 and 80 percent allocation markers, quarterly re-scoring and the 2-3 capabilities per quarter rule.
