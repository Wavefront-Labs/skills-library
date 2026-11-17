---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.optimisation-recommendations
name: optimisation-recommendations
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, optimisation-recommendations, savings-backlog, recommendation-workflow]
level: practitioner
status: docs-checked
description: "Turn optimisation recommendations into realised savings: strategy and thresholds, estimate value and effort, prioritise, agree owners, track outcomes."
sources: ["https://www.finops.org/framework/capabilities/workload-optimization/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Operationalising optimisation recommendations

The FinOps Framework Workload Optimization capability says the key gap is between identifying technically possible
optimisations and realising value; closing it needs agreed priorities, timelines and accountability across FinOps,
Engineering and other personas.

## Steps
1. **Strategy**: write a usage optimisation strategy with the priority usage areas, thresholds for taking action so
   effort is not wasted on trivial items, target KPIs and tradeoff guidelines. Set the thresholds yourself; the
   Framework gives no numbers.
2. **Generate** recommendations from billing data, monitoring and observability, and native provider and
   infrastructure-as-code tooling; make them actionable and relevant to the receiving persona.
3. **Estimate** the potential saving of each (and effects on performance and sustainability) and the cost and effort
   to act, including labour and operational impact.
4. **Prioritise** with a consistent ranking method, comparing benefit against engineering time and organisational
   priorities; weigh this against Rate Optimization options.
5. **Share and agree** with Engineering realistic timelines and accountability for each accepted recommendation.
6. **Track** each recommendation from identification to resolution, document it consistently, and compare actual
   impact with the estimate.
7. **Refine** the strategy from the actual versus estimated results.

## Gotchas
- Rightsizing can require recreating resources and cause disruption; coordinate with Engineering. Check longer-cycle
  usage peaks (month-end, quarterly) before reducing (Framework).
- Informal, untracked recommendations are the Crawl pattern; no one learns whether they worked.

## Verify
- [ ] The share of recommendations acted on trends up and time to resolution trends down (Framework KPI wording).
- [ ] Realised, not only identified, savings are reported (see `realised-savings`).

## Checked
Confirmed on the FinOps Framework Workload Optimization page: strategy and thresholds, recommendation generation,
value and effort estimates, prioritisation, accountability, tracking through resolution, rightsizing cautions.
Removed: AWS Cost Optimization Hub, Azure Advisor and Google Recommender specifics and commands (pages unreadable),
the savings x confidence / effort formula, the 50 dollar filter, the 30-day SLA, and the CPU and memory agent advice.
Method: docs-checked 2026-11-09 against finops.org Framework Workload Optimization capability page
