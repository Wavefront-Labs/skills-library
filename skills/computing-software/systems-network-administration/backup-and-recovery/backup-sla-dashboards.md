---
id: computing-software.systems-network-administration.backup-and-recovery.backup-sla-dashboards
name: backup-sla-dashboards
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-sla-dashboard, backup-monitoring, rpo-compliance, kpi, reporting, grafana]
level: practitioner
status: draft
description: "Build a backup SLA dashboard: per-tier success rate, RPO compliance, restore test results and capacity, with data from backup tool APIs and honest metric definitions."
sources:
  - https://helpcenter.veeam.com/docs/backup/vbr_rest/overview.html
  - https://grafana.com/docs/grafana/latest/dashboards/
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Backup SLA dashboards

**Purpose:** show management and auditors, at a glance, whether each protection tier meets its RPO and whether restores actually work.

## Metrics that matter (define them in writing)
| Metric | Definition | Target example |
|---|---|---|
| RPO compliance | % of in-scope systems whose newest good restore point is younger than the tier RPO | Gold 100% < 4 h, Silver > 99% < 24 h |
| Job success rate | Successful + warning runs / all runs, last 30 days | > 98% |
| Unprotected systems | Systems in CMDB/inventory with no backup | 0 |
| Restore test pass rate | Passed tests / scheduled tests, quarter | 100% |
| Measured RTO | Time from restore start to app validated, per test | Under tier RTO |
| Immutable copy coverage | % of tier with a copy in immutable/offline storage | 100% for Gold |
| Repository headroom | Days until full at current growth | > 90 days |

"Success rate" alone hides a VM that has failed every night for a week. RPO compliance per system is the headline number.

## Data sources
- Veeam: REST API (`/api/v1/sessions`, `/api/v1/backupObjects`) or Veeam ONE reports; other tools have similar APIs or CLI JSON output.
- Inventory: vCenter/Hyper-V/CMDB lists to compute unprotected systems.
- Restore tests: a simple table (system, date, result, measured time) from the test runbook.

## Build
- Collect into a database or Prometheus (see backup metrics exporters), visualise in Grafana or Power BI.
- One row per tier; red/amber/green on RPO compliance; drill-down to failing systems with ticket links.
- Trend lines (90 days) for success rate and capacity.

## Gotchas
- Exclude retired systems promptly or compliance looks worse than reality.
- Warnings count as success only if the restore point is usable; treat "warning: guest processing failed" on databases as failure.

## Verify
Pick three systems at random and check that the dashboard's last-good-backup time matches the backup console.
