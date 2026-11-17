---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-rollback
name: migration-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-migration, migration-rollback, rollback-plan, point-of-no-return, reverse-replication]
level: practitioner
status: draft
description: "Plan migration rollback: decision criteria, point of no return, reverse data sync, DNS and connection switch-back, and rehearsing the rollback."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-replatforming-cots-applications/cutover.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/migration-considerations/migrate/promote", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Migration rollback plan

## Steps
1. **Rollback triggers** written before cutover: failed smoke tests, error rate or latency
   beyond threshold for N minutes, data validation mismatch, critical integration failing.
   Name who decides (single accountable person) and the decision deadline.
2. **Point of no return**: the moment after which rolling back loses data or costs more than
   fixing forward (e.g. once new writes land only in the target with no reverse sync).
   Push it as late as possible.
3. **Preserve the source**: keep source systems intact and read-only (not deleted) until
   hypercare ends; snapshots before cutover.
4. **Reverse data path**: for online migrations configure reverse CDC from target to
   source after cutover so new writes are kept if you go back. If not possible, accept and
   document data loss window or plan a manual re-key.
5. **Switch-back mechanics**: lower DNS TTLs (e.g. 60 s) 24-48 h before cutover; keep old
   load balancer and config; feature flags or connection strings switchable without redeploy.
6. **Rehearse** rollback in a dress rehearsal, timed, just like the forward path.

## Gotchas
- Clients caching DNS or connection pools ignore low TTLs; plan restarts.
- Integrations with third parties (IP allow-lists, certificates) may not switch back quickly.

## Verify
- [ ] Rollback rehearsed with timing recorded.
- [ ] Go/no-go checklist includes rollback criteria and decision owner.
