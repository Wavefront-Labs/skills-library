---
id: computing-software.cloud-infrastructure-engineering.aws.savings-plans-compute-vs-ec2-instance
name: savings-plans-compute-vs-ec2-instance
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, savings-plans, compute-savings-plan, ec2-instance-savings-plan, savings-plan-recommendations, commitment, cost-optimization]
level: practitioner
status: docs-checked
description: "Size and buy AWS Savings Plans: Compute vs EC2 Instance plans, how the hourly commitment is applied after RIs, reading recommendations and layering purchases."
sources: ["https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-recommendations.html", "https://docs.aws.amazon.com/savingsplans/latest/userguide/sp-applying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Savings Plans: Compute vs EC2 Instance

## 1. Plan types
- A Savings Plan is a commitment to an amount of compute (measured per hour) for one year (365 days) or three years (1,095 days), paid All upfront, Partial upfront or No upfront. Prices for covered usage stay the same through the term. The page says savings go up to 72%; for current rates see the AWS Savings Plans pricing page.
- **Compute Savings Plans**: Amazon EC2 usage regardless of instance family, size, OS, tenancy or Region, and also AWS Fargate and AWS Lambda.
- **EC2 Instance Savings Plans**: tied to an instance family in a Region (the page's example is "r5 family in us-east-1"); the EC2 Instance plan has a higher savings percentage than Compute in the page's illustrative example.
- **SageMaker AI Savings Plans**: SageMaker AI instance usage regardless of family, size, component or Region.
- The eligible services list is on the "Services eligible for Savings Plans benefits" page.

## 2. How the commitment applies each hour
- Savings Plans apply after EC2 Reserved Instances.
- EC2 Instance plans apply before Compute plans because Compute plans have broader applicability.
- In a consolidated billing family they apply first to the owner account, then to other accounts, only if sharing is enabled.
- Within the hour, the commitment goes to the usage with the highest savings percentage first (savings percentage = Savings Plans rate vs current On-Demand rate). On ties, the first usage with the lowest Savings Plans rate. This continues until usage or commitment runs out; the rest is billed On-Demand.
- Each hour's commitment can only be used within that hour and cannot be carried over.

## 3. Sizing from recommendations
```bash
aws ce get-savings-plans-purchase-recommendation --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR --payment-option NO_UPFRONT --lookback-period-in-days SIXTY_DAYS \
  --account-scope PAYER
```
- Same data in the Billing and Cost Management console under Savings Plans, Recommendations. With Organizations you can view it from the management or a member account.
- Summary metrics: Monthly On-Demand spend (includes active plans you own), Estimated monthly spend (recommended commitment plus usage still On-Demand because of hour-to-hour variation), Estimated monthly savings (net).
- API lookback values: `SEVEN_DAYS`, `THIRTY_DAYS`, `SIXTY_DAYS`; plan types `COMPUTE_SP`, `EC2_INSTANCE_SP`, `SAGEMAKER_SP`, `DATABASE_SP`; account scope `PAYER` or `LINKED`.
- When billing transfer is the bill source, estimated savings may not match CUR or Cost Explorer because recommendations ignore Billing Conductor custom data; the recommended commitment stays accurate.
- Judgement (not from the pages): the commitment is a per-hour floor, so exclude one-off spikes and planned reductions before buying, and consider buying in tranches so plans expire at different times.

## Verify
- [ ] Utilisation and coverage reviewed in Cost Explorer (the Savings Plans guide says you manage plans with recommendations, performance reporting and budget alerts there).
- [ ] Purchase note records lookback, term, payment option and excluded usage.

## Method
Rewritten from the three cited Savings Plans pages; the CLI command was checked against the Cost Explorer API model. Discount percentages by plan, return-window rules, service exclusions and target utilisation figures were not on the pages and were removed.

## Checked
Checked 2026-11-08 against the three cited Savings Plans User Guide pages.
Method: docs-only read of cited pages, 2026-11-08
