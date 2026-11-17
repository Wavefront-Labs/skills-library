---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-review-cadence
name: cost-review-cadence
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-practice, cost-review-cadence, operating-rhythm, cost-reviews]
level: practitioner
status: draft
description: "Set the FinOps operating cadence: daily anomaly checks, weekly team reviews, monthly business reviews, quarterly forecasts and commitments, with agendas and inputs."
sources: ["https://www.finops.org/framework/capabilities/finops-practice-operations/", "https://www.finops.org/framework/phases/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operating cadence and cost reviews

## Rhythm
| Cadence | Who | Content |
|---|---|---|
| daily (automated) | FinOps + owners | anomaly alerts, budget threshold alerts, commitment expiries |
| weekly | team leads / champions | spend trend vs forecast, top movers, open recommendations, tag compliance |
| monthly | product owners, finance, engineering managers | month close vs budget and forecast, variance drivers, unit costs, savings realised, chargeback |
| quarterly | executives, finance, procurement | forecast refresh, commitment strategy and purchases, KPI and maturity progress, roadmap |
| annually | leadership | budgets, contract negotiation (EDP/MACC), strategy |

## Steps
1. **Standard agenda and pack** per meeting; data pre-generated from the reporting platform.
2. **Inputs before the meeting**: owners annotate variances in advance so meetings decide, not discover.
3. **Actions tracked** in a backlog with owners and dates; review status at the next meeting.
4. **Align to finance calendar**: month close dates, forecast submission windows, budget cycle.
5. **Keep it short**: 30 minutes for weekly reviews; skip when nothing changed.

## Gotchas
- Monthly-only reviews catch overspend 4-6 weeks late; daily anomaly coverage matters.
- Reviews without engineering owners present turn into finance-only reporting.

## Verify
- [ ] Calendar of reviews published with attendees.
- [ ] Action log shows closure rate.
