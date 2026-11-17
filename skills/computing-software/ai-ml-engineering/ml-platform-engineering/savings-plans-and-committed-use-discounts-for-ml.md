---
id: computing-software.ai-ml-engineering.ml-platform-engineering.savings-plans-and-committed-use-discounts-for-ml
name: savings-plans-and-committed-use-discounts-for-ml
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform, sagemaker-savings-plans, committed-use-discounts, reserved-capacity, finops, gpu-cost]
level: practitioner
status: draft
description: "Cut steady ML compute cost with commitments: SageMaker Savings Plans, EC2 plans and reservations, GCP committed use discounts, Azure reservations, sized from usage baselines."
sources:
  - https://aws.amazon.com/savingsplans/ml-pricing/
  - https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html
  - https://cloud.google.com/compute/docs/instances/committed-use-discounts-overview
  - https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Savings Plans and committed-use discounts for ML

**Goal:** the steady baseline of ML compute is bought at committed prices, without paying for commitments nobody uses.

## What applies to what (AWS)
- **SageMaker Savings Plans:** commit to $/hour for 1 or 3 years; discount applies automatically to eligible SageMaker ML instance usage (Studio notebooks, processing, training, real-time and batch inference, and other eligible components) across instance families, sizes and regions.
- **Compute Savings Plans:** EC2, Fargate, Lambda - not SageMaker. Use for self-managed GPU fleets on EC2/EKS.
- **EC2 Instance Savings Plans / Reserved Instances:** deeper discount, locked to family and region.
- **Capacity Blocks / reservations:** guarantee GPU capacity for a window; a capacity product, not a discount on general usage.

## Google Cloud
- Resource-based CUDs for vCPU, memory, GPUs and local SSD (1 or 3 years, per region); GPU CUDs typically require attached reservations.
- Spend-based (flexible) CUDs on some services; check Vertex AI eligibility for your usage types.

## Azure
Reservations (1/3-year) for specific VM sizes, including GPU series, and Azure savings plan for compute for flexible hourly commitments.

## Sizing method
1. Pull 3-6 months of hourly usage by service (Cost Explorer, BigQuery billing export, Cost Management).
2. Find the floor: usage present nearly every hour (e.g. inference endpoints, always-on training clusters).
3. Commit to ~70-90% of that floor, not the average - peaks belong on on-demand or spot.
4. Ladder commitments (buy in tranches every quarter) to adapt to growth and new instance generations.
5. Account for roadmap changes: migrating to Inferentia/Trainium or a new GPU generation can strand family-specific commitments; flexible plans reduce that risk.

## Monitor
Track utilisation (percentage of commitment used) and coverage (percentage of eligible usage covered) monthly; utilisation below ~95% means over-commitment. Use provider recommendations as input, not as the decision.

## Verify
- [ ] Commitment utilisation and coverage reported monthly.
- [ ] Commitments match a documented baseline analysis.
