---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.rightsizing-in-infrastructure-code
name: rightsizing-in-infrastructure-code
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac, iac-cost, rightsizing, finops, compute-optimizer, azure-advisor, instance-types, graviton, infracost]
level: advanced
status: draft
description: "Turn rightsizing recommendations into reviewed IaC changes: gather utilisation evidence, parameterise sizes per environment, roll out safely, and prove savings without performance regressions."
sources: ["AWS Compute Optimizer User Guide (https://docs.aws.amazon.com/compute-optimizer/latest/ug/)", "Microsoft Learn - Azure Advisor cost recommendations: right-size or shut down underutilized VMs", "FinOps Foundation - Rightsizing capability (https://www.finops.org/framework/capabilities/)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rightsizing in infrastructure code

Goal: oversized instances, databases and volumes get smaller (or a cheaper family) through the
normal IaC change process, backed by utilisation data, with a rollback path.

## 1. Evidence
- AWS Compute Optimizer (EC2, ASG, EBS, Lambda, RDS, ECS on Fargate): `aws compute-optimizer get-ec2-instance-recommendations --output json` → `finding` (`Overprovisioned`), options with projected utilisation and savings. Enable enhanced infrastructure metrics (3 months lookback) for accuracy; install the CloudWatch agent for memory metrics or recommendations ignore memory.
- Azure Advisor cost recommendations; GCP Recommender (`gcloud recommender recommendations list --recommender=google.compute.instance.MachineTypeRecommender`).
- Your own: p95 CPU and p95 memory over ≥14 days including month-end peaks. Rule of thumb: p95 CPU < 40% and memory < 50% = candidate for one size down.

## 2. Make sizes code parameters
```hcl
variable "app_instance_type" {
  type = map(string)
  default = { prod = "m7g.large", stage = "t4g.medium", dev = "t4g.small" }
}
resource "aws_launch_template" "app" {
  instance_type = var.app_instance_type[var.env]
}
```
Hard-coded sizes scattered across modules make rightsizing a hunt; one variable per workload
per environment makes it a one-line PR. Record why in a comment or ADR link.

## 3. Change safely
- Instance type change on a standalone EC2 = stop/start (downtime); in an ASG = new launch template version + instance refresh (rolling, with `min_healthy_percentage`).
- Architecture change (x86 → Graviton/ARM) needs ARM images and dependencies; treat as a migration, not a resize.
- RDS class change: apply in the maintenance window or `apply_immediately` with Multi-AZ failover (short interruption). Storage can grow but not shrink in place.
- EBS: `gp2` → `gp3` is an online modification and usually cheaper; set IOPS/throughput explicitly.
- Kubernetes: rightsizing requests/limits (VPA recommendations) is the equivalent; node sizes follow.

## 4. Review in the PR
Infracost comment shows the monthly delta; include the utilisation graph/screenshot and the
rollback (revert PR). Roll out stage first, observe a full business cycle, then prod.

## 5. Prove it
- Compare cost (tagged by workload) for the 30 days before/after.
- Watch SLOs and saturation (CPU steal, memory pressure, credit balance on burstable types).

## Gotchas
- Burstable (`t`) instances look idle on average but depend on CPU credits; check credit balance before moving to them.
- Commitments (Savings Plans/RIs) may cover the old size; resizing outside the commitment's scope can *raise* cost. Check coverage first.
- Autoscaling groups already absorbing load: rightsizing the type may just change instance count; look at total capacity.

## Verify
- [ ] Recommendation, PR, and post-change cost/performance comparison are linked in the change record.
- [ ] After a full cycle, no SLO regression and the cost report shows the projected saving.
