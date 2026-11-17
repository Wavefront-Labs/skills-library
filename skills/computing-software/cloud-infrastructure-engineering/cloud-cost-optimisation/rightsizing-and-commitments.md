---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments
name: rightsizing-and-commitments
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-allocation, tagging, showback, chargeback, rightsizing, compute-optimizer, azure-advisor, gcp-recommender, savings-plans, reserved-instances, committed-use-discounts, spot-instances, preemptible, graviton, arm64, unit-economics, cur, focus, kubecost, opencost, storage-tiering, nat-gateway, egress]
level: practitioner
status: draft
description: "Cut cloud spend in the right order: allocate costs by tag, remove waste, rightsize from utilisation data, then cover the stable baseline with Savings Plans/RIs/CUDs and use spot."
sources: ["FinOps Foundation - FinOps Framework and FOCUS specification", "AWS docs - Savings Plans User Guide and Compute Optimizer", "Microsoft Learn - Azure reservations and savings plan for compute", "Google Cloud docs - Committed use discounts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rightsizing and commitments — see it, shrink it, then commit

**Goal:** every dollar is attributed to an owner, idle and oversized resources are removed
first, and only then is the remaining steady baseline covered by discounted commitments,
with spot for interruptible work and a unit-cost metric to show progress.

## 1. Allocate before optimising
- Required tags/labels: `owner`, `cost-centre`, `env`, `service`. Enforce with AWS Organizations tag
  policies / Azure Policy / GCP org policy; **activate cost-allocation tags** in AWS
  Billing (tags are not in billing data until activated, and not retroactively).
- Account-per-workload structure makes allocation mostly free; tags then subdivide.
- Export billing data: AWS CUR 2.0 (or FOCUS export) to S3 + Athena, Azure Cost Management
  exports, GCP Billing export to BigQuery. Normalise across clouds with the **FOCUS** schema.
- Shared costs (networking, platform, support) split by a stated rule (proportional to direct spend, or usage).
- Kubernetes: OpenCost/Kubecost allocate node cost to namespaces by requests.
- Showback monthly to teams; anomaly detection (AWS Cost Anomaly Detection, Azure/GCP
  equivalents) alerts the owner within a day.

## 2. Remove waste (cheapest wins)
- Unattached EBS volumes / managed disks / persistent disks, old snapshots, idle load
  balancers, unassociated public IPv4 (charged on AWS since 2024), stopped instances with
  big disks.
- Non-prod schedules: off nights and weekends cuts ~65-70% of running hours.
- Storage lifecycle: S3 Intelligent-Tiering or lifecycle rules to IA/Glacier; delete
  incomplete multipart uploads; log retention limits in CloudWatch/Log Analytics.
- Network: NAT gateway processing and cross-AZ/egress transfer often hide in "EC2-Other";
  add VPC gateway endpoints for S3/DynamoDB (free) and keep chatty traffic in-zone.

## 3. Rightsize from data
- Use 14+ days (ideally 30) of utilisation at peak, not averages: CPU p95, memory
  (needs the CloudWatch agent / Azure Monitor agent — memory is not a default metric on
  most VMs), network, IOPS.
- Tools: AWS Compute Optimizer, Azure Advisor, GCP Recommender; for Kubernetes, VPA in
  recommend mode and request-vs-usage dashboards. Bin-packing requests is where K8s money goes.
- Move instance families as well as sizes: current generation, **ARM (Graviton, Ampere/
  Cobalt, Axion)** commonly 20-40% better price-performance — benchmark your workload.
- Databases: rightsize, consider serverless/auto-pause tiers for spiky dev, and gp3 over gp2 (cheaper and IOPS independent of size).

## 4. Commit for the baseline
| Option | Flexibility | Typical discount (check current pricing) |
|---|---|---|
| AWS Compute Savings Plan | any region/family/OS, EC2+Fargate+Lambda | up to ~66% |
| AWS EC2 Instance Savings Plan | one family in one region | up to ~72% |
| AWS RIs (RDS, ElastiCache, OpenSearch, Redshift) | engine/class-specific | varies |
| Azure savings plan for compute / Reservations | hourly commit / specific SKU | up to ~65% / ~72% |
| GCP CUDs (resource-based or spend-based flexible) | region-bound / cross-family | roughly 28-70% |

- Commit to the **floor** of the last 30-90 days of steady usage after rightsizing,
  not the average. Target 70-85% coverage with near-100% utilisation; the rest stays on-demand.
- Ladder purchases (e.g. a tranche each month or quarter) so commitments expire on a
  staggered schedule and track change. 1-year no-upfront is the lowest-risk start; 3-year
  all-upfront maximises discount.
- Commitments are bought centrally (payer/billing account) and shared; track coverage and utilisation weekly.

## 5. Spot and preemptible
- Up to ~90% off for interruptible work: CI runners, batch, stateless workers, K8s node
  pools behind PDBs. AWS gives a 2-minute notice; GCP/Azure ~30 seconds.
- Diversify across many instance types and zones (`capacity-optimized` / price-capacity
  allocation, Karpenter with broad requirements).

## 6. Unit economics
Track cost per business unit — per 1,000 requests, per active customer, per GB processed.
Total spend rising with revenue is fine; unit cost rising is the problem.

## Gotchas
- Buying commitments before rightsizing locks in waste for 1-3 years.
- Savings Plans apply to the highest-discount usage first; adding an Instance SP on top of Compute SP can shift where savings land, confusing showback.
- Spot discounts do not stack with Savings Plans; covering spot-heavy fleets wastes commitment.
- Migrating to ARM or a new family can strand existing RIs; check exchange rules.
- Tags on a resource do not tag its data transfer or snapshots automatically.

## Verify
- [ ] Over 90% of spend is attributable to an owner via account or tag.
- [ ] A waste report (unattached disks, idle IPs, old snapshots) runs monthly and trends to zero.
- [ ] Top 20 instances/services have been reviewed against p95 utilisation in the last quarter.
- [ ] Commitment coverage and utilisation are reported, with utilisation above ~95%.
- [ ] Interruptible workloads run on spot with diversified pools.
- [ ] A unit-cost metric is published monthly alongside total spend.
