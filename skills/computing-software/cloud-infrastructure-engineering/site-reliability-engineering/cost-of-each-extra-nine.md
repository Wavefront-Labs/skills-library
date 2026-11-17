---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.cost-of-each-extra-nine
name: cost-of-each-extra-nine
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [cost-of-nines, reliability-cost-curve, availability-target, embracing-risk, nines, opportunity-cost, sre]
level: practitioner
status: docs-checked
description: "Price an extra nine of availability: downtime budgets per nine, redundancy and feature-velocity cost, and the revenue-at-risk arithmetic that decides whether it pays."
sources: ["https://sre.google/sre-book/embracing-risk/", "https://sre.google/sre-book/availability-table/", "https://sre.google/workbook/implementing-slos/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The cost of each extra nine

Each extra nine costs more while the user-visible gain shrinks. The job is to show, with numbers, where
the curve stops paying.

## Downtime budget per nine
| Target | Per 30 days | Per quarter | Per year |
|---|---|---|---|
| 99% | 7.2 h | 21.6 h | 3.65 d |
| 99.9% | 43.2 min | 2.16 h | 8.76 h |
| 99.95% | 21.6 min | 1.08 h | 4.38 h |
| 99.99% | 4.32 min | 12.96 min | 52.6 min |
| 99.999% | 25.9 s | 77.8 s | 5.26 min |

Compare each budget with your measured time to detect and mitigate an incident. If one incident uses most of
the budget for a target, that target needs automated failover rather than a human in the loop.

## What each nine costs
1. **Redundant capacity**: spare capacity per zone and across regions, plus cross-region consistency work.
2. **Opportunity cost**: engineers building failover instead of features; slower release cadence (bigger
   canaries, longer soak).
3. **Process cost**: tighter on-call response, more drills, stricter change control.
4. **Dependency ceiling**: you cannot exceed the availability of hard serial dependencies; 3 deps at 99.95%
   cap you near 99.85% unless you design around them.

## Decide with revenue at risk
```
value_of_nine = revenue_per_minute * (budget_minutes_now - budget_minutes_next) * fraction_of_users_affected
cost_of_nine  = extra_infra_per_year + engineer_years * loaded_cost + velocity_loss_estimate
```
Worked example (from the SRE Book): a service with $1M revenue moving 99.9% -> 99.99% gains 0.09%
availability, worth $1M * 0.0009 = $900. If the cost of the extra nine is above that, it exceeds the projected revenue. Unless outages also cause churn or SLA penalties, the
extra nine is not worth a single engineer. Add SLA credit exposure and churn estimates explicitly; do not
hand-wave them.

## Gotchas
- Measure the *ISP and client* background error rate first; the SRE Book reports typical ISP background error rates of 0.01% to 1%, and errors below that fall within the noise of a user's connection.
- Each nine also shrinks the error budget for releases, so velocity drops even when nothing breaks.
- Present a curve (target vs cost) to the product owner, not a single recommendation.

## Checked

2026-11-01. Confirmed against the SRE Book pages Embracing Risk (the 99.9% -> 99.99% worked example, the ISP
background error range, the one-more-nine question) and Availability Table (every downtime figure in the table above).
Removed: the exponential-cost claim, the phone-reliability claim, the multi-region doubling claim, the 5 minute ack
figure and the 20 minute incident example (it contradicted the 12.96 minute quarterly budget).
Method: documentation only; no commands were run.

## Verify
- [ ] Table of target vs downtime vs current MTTR produced.
- [ ] Cost and value estimated per candidate nine and signed off by the product owner.
- [ ] Hard dependency availability product computed and below the proposed target.
