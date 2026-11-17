---
id: computing-software.cloud-infrastructure-engineering.aws.defining-rto-and-rpo-with-business-impact-analysis
name: defining-rto-and-rpo-with-business-impact-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, business-impact-analysis, rto-rpo-targets, disaster-recovery, resilience-hub-policy, tiering]
level: advanced
status: docs-checked
description: "Set RTO and RPO per workload from a business impact analysis, tier workloads, map tiers to AWS DR strategies and data replication, and record them as Resilience Hub policies."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/business-continuity-plan-bcp.html", "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_planning_for_recovery_objective_defined_recovery.html", "https://docs.aws.amazon.com/resilience-hub/latest/userguide/resiliency-policies.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining RTO and RPO with a business impact analysis

## 1. Terms
- **RTO** (recovery time objective): maximum acceptable time from disruption to restored
  service.
- **RPO** (recovery point objective): maximum acceptable data loss measured in time.
- Also capture **MTD** (maximum tolerable downtime) and the minimum service level during
  recovery (degraded mode acceptable?).

## 2. Business impact analysis (BIA) steps
1. List business processes and the workloads (and dependencies) supporting each.
2. For each process, estimate impact over time if unavailable: revenue per hour, contractual
   penalties/SLAs, regulatory obligations, safety, reputation. Use time buckets (15 min,
   1 h, 4 h, 24 h, 72 h).
3. Find where impact becomes unacceptable: that is the RTO. Ask how much data re-entry or
   loss is tolerable: that is the RPO.
4. Identify dependencies (identity, DNS, payment provider, shared databases); a workload's
   effective RTO cannot be better than its slowest critical dependency.
5. Get sign-off from the business owner, not just engineering. Review annually or when
   the business changes.

## 3. Tiering
| Tier | Example | RTO | RPO | Typical AWS strategy |
|---|---|---|---|---|
| 0 / critical | payments, auth | minutes | near zero | multi-site active/active or warm standby with continuous replication (Aurora Global, DynamoDB global tables) |
| 1 | customer-facing apps | < 1-4 h | minutes | warm standby or pilot light; DRS for servers |
| 2 | internal tools | < 24 h | hours | backup and restore with IaC rebuild |
| 3 | archives, batch | days | 24 h | backup and restore |
Cost rises steeply toward tier 0; the BIA justifies the spend.

## 4. Turn targets into engineering requirements
- RPO drives replication: async cross-region replication lag must be well under RPO
  (S3 RTC replicates 99.9 percent of objects within 15 minutes, Aurora Global Database typically under a second, AWS Backup cross-region copy
  frequency = RPO for backup-based tiers).
- RTO drives automation: restore and failover runbooks, IaC for rebuild, pre-provisioned
  capacity (warm standby), DNS TTLs, data restore durations (large DB restores can take
  hours: measure).
- Include detection and decision time in RTO (how long until someone declares a disaster).

## 5. Record and verify
- Resilience Hub resiliency policy per tier with RTO/RPO for software, hardware, AZ and Region disruptions; assess apps against it (`create-resiliency-policy`,
  `start-app-assessment`).
- DR tests measure achieved RTO/RPO; record results and gaps.

## Verify
- [ ] Every production workload has a signed-off tier with RTO/RPO and dependency list.
- [ ] Replication and backup frequencies satisfy RPO; last DR test met RTO including decision time.
- [ ] Resilience Hub assessment shows policy compliance or tracked remediation.

## Checked

2026-10-28

Confirmed: S3 RTC 15-minute figure (S3 User Guide), Aurora global database replication latency (Aurora User Guide), Resilience Hub disruption types Software/Hardware/AZ/Region and the two API operations (Resilience Hub guide, botocore).

Removed: the 'S3 RTC 15 min SLA' wording (guide gives 99.9 percent within 15 minutes); the application/infrastructure disruption grouping.

Method: documentation only; no commands were run.
