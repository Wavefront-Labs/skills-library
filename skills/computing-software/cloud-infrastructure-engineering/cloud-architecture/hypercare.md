---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.hypercare
name: hypercare
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-migration, hypercare, decommissioning, post-migration, source-retirement]
level: practitioner
status: draft
description: "Run post-migration hypercare and decommission the source: heightened monitoring, exit criteria, data retention, and actually switching the old estate off."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/migrate/migration-considerations/optimize/decommission", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-retiring-applications/welcome.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hypercare and decommissioning the source

## Hypercare (typically 1-4 weeks)
1. **Staffing**: migration team plus app owners on an elevated rota; daily stand-up; a
   single channel for issues.
2. **Monitoring**: compare against pre-migration baselines (latency, error rate, batch
   durations, business KPIs such as orders per hour). Watch month-end and batch cycles
   that have not run yet in the new environment.
3. **Triage**: log every issue with migration-caused vs pre-existing tag.
4. **Exit criteria**: no Sev1/Sev2 for N days, full business cycle completed (including a
   month-end), backups and DR tested in target, runbooks handed to BAU support, cost within forecast.

## Decommissioning
1. **Confirm no traffic** to source (flow logs, DB connections, job schedules) for an agreed period.
2. **Data retention**: final backup or archive per retention policy; legal hold check.
3. **Shut down, then wait** (e.g. 2 weeks powered off) before deletion to catch hidden dependencies.
4. **Remove**: servers, storage, firewall rules, DNS records, monitoring, CMDB entries,
   licences (and reclaim or cancel them), support contracts, backup jobs.
5. **Record savings** and confirm with finance; double running ends only when billing stops.

## Gotchas
- Decommissioning gets deprioritised once the new system works; double running persists for months.
- Licence true-ups and hardware maintenance contracts continue billing until cancelled.

## Verify
- [ ] Hypercare exit criteria met and signed off.
- [ ] Source decommission checklist complete with savings recorded.
