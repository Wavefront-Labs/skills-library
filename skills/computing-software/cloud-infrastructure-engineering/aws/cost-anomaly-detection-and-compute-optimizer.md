---
id: computing-software.cloud-infrastructure-engineering.aws.cost-anomaly-detection-and-compute-optimizer
name: cost-anomaly-detection-and-compute-optimizer
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cost-anomaly, cost-anomaly-detection, compute-optimizer, rightsizing, right-sizing, cost-optimization-hub, anomaly-monitor, alert-subscription, memory-metrics, graviton-recommendations, idle-resources, ebs-rightsizing, lambda-rightsizing, ecs-rightsizing, savings-estimation, finops, ec2-recommendations, asg-recommendations, enhanced-infrastructure-metrics, memory-metrics-co]
level: practitioner
status: draft
description: "Catch spend spikes with Cost Anomaly Detection monitors and alerts, and rightsize EC2/EBS/Lambda/ECS/RDS with Compute Optimizer and Cost Optimization Hub without breaking performance."
sources: ["AWS Cost Management User Guide - Detecting unusual spend with AWS Cost Anomaly Detection", "AWS Compute Optimizer User Guide - Viewing recommendations and enabling enhanced infrastructure metrics", "AWS Cost Optimization Hub User Guide", "AWS Compute Optimizer User Guide - Metrics analyzed and the CloudWatch agent memory metric"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost Anomaly Detection and Compute Optimizer — the spike today, the oversize every month

**Goal:** a runaway NAT, a forgotten GPU instance or a mis-sized job alerts its owner within
hours; and the fleet is sized from measured utilisation, with memory included, not guesses.
(Commitment purchasing and the general rightsizing method:
`computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.rightsizing-and-commitments`.)

## 1. Cost Anomaly Detection
- **Monitors** define the scope the ML model learns per segment:
  | Monitor type | Segments by | Use |
  |---|---|---|
  | AWS services (recommended first) | each service in each account | Catches "new service started costing" |
  | Linked account | account(s) | Per-team ownership |
  | Cost category | category value | Showback-aligned |
  | Cost allocation tag | tag value | Per-application |
  One services monitor per payer + one per team dimension is typical; monitors are free.
- **Alert subscriptions**: threshold as absolute (`> $100` impact) and/or percentage
  (`> 40 %` above expected); frequency `INDIVIDUAL` (as detected, SNS/chat) for ops,
  `DAILY`/`WEEKLY` digests (email) for managers. Route SNS → Slack with the anomaly's
  root-cause fields (service, account, usage type, region).
- Detection runs ~3×/day on billing data (8–24 h lag); it needs ~10 days of history per
  segment. New accounts/services show anomalies for their first week — expected.
- Each anomaly carries **root causes** (top contributing service/account/usage type) and a
  link to Cost Explorer; mark feedback (`YES`/`NO`/`PLANNED_ACTIVITY`) to tune the model.
- EventBridge: anomalies are also emitted as events from `source: aws.ce` (copy the exact
  `detail-type` from the console's "Alert via EventBridge" option), so a rule can auto-create tickets.

## 2. Compute Optimizer
- Opt in at the **organization** level from the management account (`update-enrollment-status
  --status Active --include-member-accounts`). Analyses 14 days of CloudWatch metrics
  (CPU, network, disk, EBS I/O) — **no memory unless the CloudWatch agent publishes it**
  (`mem_used_percent` in `CWAgent` namespace, standard dimension set). Without memory, "downsize"
  recommendations are risky; enable the agent first.
- **Enhanced infrastructure metrics** (paid): 3 months lookback — needed for monthly/quarterly peaks.
- Resources: EC2 instances, ASGs, EBS volumes (gp2→gp3, over-provisioned IOPS), Lambda
  (memory), ECS on Fargate (task CPU/memory), RDS (instance class, storage), idle resources, commercial software licences.
- Findings: `Under-provisioned` (fix first — performance risk), `Over-provisioned`,
  `Optimized`, `NotOptimized` (EBS/Lambda), plus **idle** for unused resources.
- Recommendation detail includes projected utilisation, **performance risk** (0–4),
  savings/month, and **migration effort** when the target is a different family
  (e.g. Graviton `m7g` needs ARM builds). Set the **preferred CPU architecture / instance
  families** in *recommendation preferences* so suggestions match what you can run; set
  lookback and the `Inferred workload type` to tune.
- Export: `export-ec2-instance-recommendations --s3-destination-config bucket=…` (CSV) for
  bulk review; or query **Cost Optimization Hub** which aggregates Compute Optimizer +
  Savings Plans/RI + idle recommendations across accounts with de-duplicated savings and
  filters (`list-recommendations --filter ...`).

## 3. Acting on recommendations safely
1. Start with **idle** (terminate/stop; snapshot first) and **EBS gp2→gp3** (no downtime, ~20 % cheaper, same perf).
2. **Over-provisioned** EC2: modify instance type in the launch template → instance refresh
   (ASG) or stop/change/start (standalone) during a window; keep the old type for 48 h rollback.
3. Lambda memory: Compute Optimizer suggests the cheapest duration/cost point; use
   **AWS Lambda Power Tuning** (Step Functions) to confirm on your function.
4. Fargate tasks: new task definition revision with the recommended CPU/memory; watch
   `MemoryUtilization` p99 after deploy.
5. RDS: change class in the maintenance window, Multi-AZ instances fail over (~1 min).
- Guardrails: never downsize below **p99 of the last 3 months**; exclude instances with
  `Name` tag containing `batch` unless the lookback covers their schedule; check the
  recommended type is available in all AZs you use and in the DR region.
- Automate the ticketing, not the change: weekly job → one Jira per owner with savings; measure realised savings in Cost Explorer by usage type.

## 4. Metrics to watch after a change
EC2: `CPUUtilization` p95 < 70 %, `mem_used_percent` < 80 %, `NetworkIn/Out` vs baseline, EBS
`VolumeQueueLength` < 1 per 1 000 IOPS. App: p99 latency and error rate unchanged for 7 days.

## Gotchas
- Compute Optimizer ignores instances < 30 h old or with insufficient data (`Insufficient data` finding); new fleets need two weeks.
- Memory metric must be in `CWAgent` namespace with the default dimensions (`InstanceId`
  plus `ImageId`/`InstanceType` optional); custom namespaces are not read.
- Anomaly Detection does not see usage that is billed in arrears (support, some Marketplace) and treats the *first* month of a new service as noise.
- T-family "under-provisioned" often means CPU credits exhausted — fix with `unlimited` or a fixed-performance family rather than a bigger T.
- Recommendations assume the same workload; a rightsized instance has less headroom for the incident you have not had yet — keep ASG scaling healthy.
- Unconfirmed: exact EventBridge event names for anomalies and the current enhanced-metrics price — check the console/pricing.

## Verify
- [ ] A services monitor and a per-team monitor exist with INDIVIDUAL alerts to a chat channel; test by launching a `p3.2xlarge` for an hour in sandbox and confirming an alert within a day.
- [ ] Compute Optimizer shows memory data for EC2 (recommendation page lists "Memory" with values).
- [ ] Idle resources list reviewed monthly; count trending down.
- [ ] gp2 volumes = 0 in production accounts.
- [ ] Realised savings from applied recommendations visible in Cost Explorer by usage type month over month.
