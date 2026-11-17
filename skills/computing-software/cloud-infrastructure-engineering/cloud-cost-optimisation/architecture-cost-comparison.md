---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.architecture-cost-comparison
name: architecture-cost-comparison
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-estimation, architecture-cost-comparison, design-alternatives-cost, cost-model, what-if-analysis]
level: practitioner
status: docs-checked
description: "Compare the cost of architecture options before deciding: shared load model, per-option cost model, scenarios, pricing models, ranges and a decision record."
sources: ["https://www.finops.org/framework/capabilities/planning-estimating/", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/select-the-best-pricing-model.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost comparison of architecture options

The FinOps Planning & Estimating capability treats estimating as exploratory scenario work that feeds forecasting and
optimisation (architecting for cloud, workload optimisation, onboarding workloads). No single estimating method fits
every situation, so agree parameters, scenarios and documentation expectations up front.

## Steps
1. **Shared load model**: requests per day and peak per second, payload size, data stored and growth, data transfer
   paths, users, environments. Every option uses the same model.
2. **Cost model per option**, line by line: compute, storage, requests, data transfer, managed service fees, licences,
   observability, backup and DR, support, plus the people cost to operate.
3. **Scenarios**: cost each option at today's volume and at higher volumes you expect; find crossover points (for
   example serverless vs containers, managed vs self-hosted). Reuse similar existing applications as a starting point
   where your architectures are consistent.
4. **Pricing model**: cost each option under the purchasing models that apply (on-demand, Spot, commitment discounts such
   as AWS Savings Plans or Reserved Instances, geographic selection, third-party agreements). Use the provider's own
   recommendation tooling (for example AWS Cost Explorer recommendations) and an hourly usage view to spot elasticity
   that suits Spot.
5. **Range and confidence**: state each estimate as a range with a confidence level, not a single figure, and keep a
   lightweight register so one estimate carries across prioritisation, commercial and architecture gates.
6. **Non-cost factors**: reliability, time to market, lock-in.
7. Record in an ADR with the spreadsheet linked; revisit at the next scale point.

## Gotchas
- Comparing an optimised option A with a naive option B.
- Ignoring per-request and per-GB charges that grow with volume.
- Forgetting non-production environments.

## Verify
- [ ] Each option is costed at three scale points with assumptions listed and a range stated.

## Checked
2026-11-09: confirmed the scenario/estimating, similar-applications and range-with-confidence wording on the FinOps
Planning & Estimating page and the list of pricing models and recommendation tooling on the AWS Well-Architected
"Select the best pricing model" page. Removed: the 30-50% non-production figure and the claim that data transfer or
logging usually dominates; the Azure design-principles source (404).
Method: documentation only; no commands were run.
