---
id: computing-software.cloud-infrastructure-engineering.aws.aws-pricing-calculator-estimates
name: aws-pricing-calculator-estimates
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, pricing-calculator, cost-estimation, bill-estimates, workload-estimates, architecture-costing]
level: practitioner
status: draft
description: "Defensible estimates with AWS Pricing Calculator: public estimates with groups and sharing, in-console workload and bill estimates with your discounts, and common omissions."
sources: ["AWS Pricing Calculator User Guide - Generating estimates", "AWS Billing and Cost Management User Guide - Pricing Calculator in the console (bill estimates and workload estimates)", "AWS Pricing Calculator User Guide - Sharing and exporting estimates"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AWS Pricing Calculator estimates

## Two tools
| | calculator.aws (public) | Pricing Calculator in the Billing console |
|---|---|---|
| Account needed | no | yes |
| Prices | public list prices | can apply your discounts and commitments (Savings Plans, RIs) |
| Outputs | shareable link, CSV/PDF/JSON export | workload estimates and **bill estimates** that model changes to your actual bill |
| Use | early design, proposals | budgeting changes to an existing estate |

## Building an estimate
- Create **groups** per tier or environment (web, data, prod, non-prod) so totals map to the architecture.
- Per service choose region, usage pattern (e.g. EC2 baseline + peak hours; Lambda requests x duration x memory), pricing model (On-Demand, Savings Plans, Spot, RI).
- Add services people forget:

| Often missed | Notes |
|---|---|
| Data transfer | out to internet, inter-AZ, inter-region, NAT gateway processing |
| Load balancers | LCU-hours, not just hours |
| CloudWatch | logs ingestion and storage, custom metrics, alarms |
| Backups and snapshots | AWS Backup storage, cross-region copies |
| Support plan | % of spend |
| Security services | GuardDuty, Security Hub, Config rules per evaluation |
| Public IPv4 addresses | hourly per address |

- State assumptions in each service's description (requests/day, GB/month); estimates without assumptions cannot be reviewed.

## Bill estimates (console)
- Start from your current usage, add/modify/remove workloads (e.g. "migrate 50 m5 to m7g", "add new region"), and see the projected bill with your discounts.
- Commitment modelling: add a planned Savings Plan purchase to see its effect.

## Sharing
- Public estimate links are accessible to anyone with the link; strip sensitive naming.
- Export CSV for finance spreadsheets; re-import JSON to revise.

## Gotchas
- Calculators exclude taxes and some marketplace fees.
- Monthly figures assume 730 hours.
- Prices change; date-stamp estimates and refresh before decisions.

## Verify
- [ ] Estimate has groups, assumptions per line, and includes data transfer, monitoring and support.
- [ ] After go-live, compare actuals at month 2 and record the variance.
