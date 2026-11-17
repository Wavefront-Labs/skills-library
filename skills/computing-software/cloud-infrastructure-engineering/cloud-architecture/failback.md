---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.failback
name: failback
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, failback, dr-runbook, reverse-replication, failover-procedure, dr-exit]
level: practitioner
status: draft
description: "Write the DR runbook including failback: declare, fail over, operate in DR, re-establish reverse replication, and return to primary without data loss."
sources: ["https://docs.aws.amazon.com/drs/latest/userguide/failback-overview.html", "https://learn.microsoft.com/azure/site-recovery/failover-failback-overview-modernized", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DR runbook and failback

## Runbook sections
1. **Declaration**: who can declare a disaster, criteria (expected outage > RTO budget), comms tree.
2. **Pre-checks**: DR region health, replication lag (RPO exposure), capacity, credentials.
3. **Failover steps** in dependency order: data tier promote -> app tier scale/start -> config
   switch (endpoints, secrets) -> traffic switch (DNS / global LB / routing controls) -> validation.
4. **Operate in DR**: monitoring, backups in DR, reduced features if applicable, change freeze.
5. **Failback** (often harder than failover):
   - Repair primary; **reverse replication** DR -> primary (AWS DRS failback replication, ASR
     re-protect, DB replica from new primary).
   - Wait for sync; schedule a maintenance window.
   - Quiesce writes, confirm zero lag, switch traffic back, restore original replication direction.
6. **Post-event**: incident review, update runbook, re-test.

## Practices
- Runbook as code where possible (scripts, SSM Automation, ARC readiness checks).
- Every step has owner, expected duration, verification, rollback.
- Time each rehearsal; compare to RTO.

## Gotchas
- Split-brain: old primary comes back and accepts writes. Fence it (disable writers, block network).
- DNS caches extending failback time; plan TTLs.
- Failback forgotten; the business runs in a DR region sized for emergencies.

## Verify
- [ ] Full failover and failback rehearsed in the last 12 months with timings recorded.
