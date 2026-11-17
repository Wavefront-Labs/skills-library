---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.esr-benchmark
name: esr-benchmark
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-benchmarking, esr-benchmark, effective-savings-rate, rate-optimisation-kpi, commitment-benchmark]
level: practitioner
status: docs-checked
description: "Calculate and benchmark Effective Savings Rate (ESR) for commitment discounts: on-demand equivalent data, the formula, and acting on where you sit."
sources: ["https://www.finops.org/wg/how-to-calculate-effective-savings-rate-esr/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effective savings rate benchmark

ESR is a KPI for the financial performance of discount instruments such as Reserved Instances and Savings Plans. It
compares savings actually generated with the on-demand equivalent (ODE) spend: what the usage would have cost with no
discount.

## Formula
- `ESR = cloud savings generated / ODE spend`.
- With costs to achieve the savings (tooling, service, time): `ESR = (RI and SP savings - cost to achieve) / ODE spend`.
- Equivalent form: `utilisation x coverage x discount`.

## Data needed
- Billing and usage data that includes the ODE of the discounted usage, plus commitment utilisation, coverage and
  discount versus the on-demand rate.
- ODE is not available in some common reporting tools, such as the AWS Cost Explorer console; the Cost Explorer API/CLI
  returns it.
- Use a full month as the time window. The playbook's worked example covers AWS compute only (EC2, Fargate, Lambda): ODE
  is the sum of savings-plan ODE, reserved-instance ODE and remaining on-demand spend, and the savings come from the
  savings plans and reservations utilisation calls (`aws ce get-savings-plans-utilization`,
  `get-reservation-utilization`, `get-savings-plans-coverage`).

## Benchmark and act
- Compare with peers by industry and usage; the playbook notes ESR and usage appear correlated.
- Negative ESR: a premium over on-demand, likely over-commitment or under-used commitments. Consider letting commitments
  expire or adjusting them to usage.
- Below average: automation can reduce manual commitment management.
- Above average with falling usage: ESR is measured at a point in time and fluctuates, so check it is sustainable and
  consider a mix of more flexible instruments.

## Gotchas
- Engineering choices move ESR: region, instance family, operating system, workload volatility and instrument type all
  change the discount available.
- Spend-based instruments such as Savings Plans risk over-commitment if engineering optimisation lowers usage.

## Verify
- [ ] ODE spend comes from a source that reports it, not from the discounted bill.
- [ ] Scope (services, period) is stated whenever ESR is compared.

## Checked
Confirmed against the FinOps Foundation playbook "How to Calculate Effective Savings Rate (ESR)": definition, both
formula forms, ODE data requirement and Cost Explorer limitation, full-month window, AWS compute worked example and
CLI calls, benchmarking and segment actions, engineering-choice exceptions. Removed: FOCUS and CUR column mappings, credits
inflating ESR, the "ESR methodology monthly trend" check, any percentile figures, and the benchmarking and rate-optimization
capability sources (pages not read for these claims).
Method: docs-checked 2026-11-09 against https://www.finops.org/wg/how-to-calculate-effective-savings-rate-esr/
