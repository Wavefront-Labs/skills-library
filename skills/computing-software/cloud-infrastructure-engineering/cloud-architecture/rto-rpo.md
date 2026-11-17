---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.rto-rpo
name: rto-rpo
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, rto-rpo, recovery-time-objective, recovery-point-objective, dr-strategy-selection, business-impact-analysis, dr-tiers]
level: practitioner
status: docs-checked
description: "Set RTO and RPO per workload with the business and map them to a DR strategy (backup-restore, pilot light, warm standby, active-active) with cost and complexity implications."
sources: ["https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html", "https://learn.microsoft.com/azure/well-architected/reliability/disaster-recovery", "https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Setting RTO and RPO

- **RTO**: the maximum acceptable time to restore operations after a disaster (Google: how long the
  application can be offline).
- **RPO**: the maximum acceptable data loss, measured in time. It describes only the length of time,
  not the amount or quality of data lost.

## Steps
1. Start from a business impact analysis (Google's DR planning begins there). Group workloads into
   criticality tiers; Azure says higher tiers need faster recovery and more frequent data
   protection, and each tier warrants a different level of investment. If one workload has flows
   of differing criticality, document the recovery approach for each.
2. Derive RTO and RPO per tier. Azure advises deriving them from the tier, then accounting for
   dependencies between data stores and restoring databases before the applications that need them.
   Google notes RPO varies by data: frequently modified user data may need minutes, rarely
   modified data hours.
3. **Map to strategy** (AWS whitepaper's four approaches; Azure and Google use cold/warm/hot ideas):
   | Strategy | What the sources say |
   |---|---|
   | Backup and restore | Mitigates data loss or corruption; the achievable recovery point depends on backup frequency; infrastructure must be redeployed (use IaC) |
   | Pilot light | Data replicated, core infrastructure provisioned, app servers switched off; cannot process requests until switched on and scaled |
   | Warm standby | Scaled-down but fully functional copy; handles traffic at reduced capacity at once and only needs scaling up |
   | Multi-site active/active | Serves traffic from all Regions; recovery time near zero for most disasters; the most complex and costly |
   Google: smaller RTO and RPO usually cost more to run and add administrative overhead.
4. Check that your RTO covers more than restore time. Azure says to validate delays in processes
   outside your control, such as DNS propagation, and to define DR activation criteria that
   separate a true disaster from a minor incident. AWS cautions that automatically initiated
   failover can cause loss on a false alarm, so manual initiation of automated steps is common.
5. Record the targets in the DR plan, review it about every six months (Azure) and prove it with
   drills. Test component-level and overall RTO and RPO separately (Azure).

## Gotchas
- Continuous replication does not protect against corruption or malicious deletion by itself: AWS
  says to add versioning or point-in-time recovery. With active/active, recovery from data
  corruption still has a recovery point before the disaster was discovered.
- Test restores: Azure and AWS both say a backup strategy must include testing restores.

## Verify
- [ ] Each workload has RTO and RPO signed off by its business owner.
- [ ] Last DR drill measured actuals within targets.

## Checked
2026-11-08. Confirmed against the AWS DR options whitepaper page (four approaches and their
descriptions, backup frequency sets recovery point, cautions on automatic failover, replication vs
point-in-time recovery), the Azure Well-Architected DR strategies page (criticality tiers, derive
targets, disaster thresholds, dependencies, DNS delay validation, six-monthly review, separate
component tests) and the Google Cloud DR planning guide (RTO and RPO definitions, cost
relationship, per-data RPO). Removed: the table of typical RTO and RPO figures and the "dependencies
inherit the strictest RTO" rule (not stated in the pages).
Method: documentation only; no commands were run.
