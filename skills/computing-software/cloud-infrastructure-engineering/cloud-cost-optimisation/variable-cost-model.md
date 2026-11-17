---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.variable-cost-model
name: variable-cost-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-principles, variable-cost-model, opex, decentralised-spending, cost-speed-quality]
level: intro
status: docs-checked
description: "Explain and operationalise the cloud variable cost model: consumption-based spend, cost/quality/speed trade-offs, decentralised ownership and just-in-time planning."
sources: ["https://www.finops.org/framework/principles/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The variable cost model

A FinOps Framework principle says to take advantage of the variable cost model of the cloud: an increasing amount of every
technology category is becoming consumption-based, granular and more variable. The variable model of the cloud and the fixed
cost model of the data centre each present opportunities to deliver more value.

## What changes
| Fixed-cost, plan-ahead habit | What the Framework encourages |
|---|---|
| Decide capacity once, long term | just-in-time prediction, planning and purchasing of capacity wherever valuable, to reduce waste |
| Static long-term plans | agile iterative planning in an increasing share of the technology estate |
| Reactive, infrequent clean-ups | proactive architecture and design with continuous adjustment |
| Cost owned by a central group | usage accountability pushed to the edge, with engineers owning cost from design to operations |
| Rate decisions made by each team | rate, commitment and discount optimisation centralised for scale, so engineers focus on usage |

## The trade-off
The Framework says to make conscious trade-off decisions among cost, quality and speed, and that business value, shown
by unit economics and value-based metrics, should drive technology decisions. Spending more can be right when it buys
speed or quality; record the reasoning.

## Operationalise
1. Provide cost data to teams as soon as it is available, in a form they use, so fast feedback changes behaviour.
2. Let feature and product teams manage their usage against budgets they help control, and treat cost as a first-class
   metric from the start of the development lifecycle.
3. Use trending and variance analysis to explain changes in cost.
4. Make technology decisions on cost model considerations as well as technical requirements.

## Verify
- [ ] Finance and engineering leads can each explain why last month's cost changed.
- [ ] Decisions to spend more for speed or reliability are recorded with the expected value.

## Checked
Confirmed on the FinOps Framework Principles page (read in full): variable cost model principle and its sub-points,
trade-off among cost, quality and speed, ownership at the edge, data accessibility and timeliness, centralised rate
optimisation. Removed: the "iron triangle" label, the table of capex and depreciation controls, the spot, night-time
scale-down and environment shutdown savings examples, and the book citation (not a readable source).
Method: docs-checked 2026-11-09 against finops.org Framework Principles page
