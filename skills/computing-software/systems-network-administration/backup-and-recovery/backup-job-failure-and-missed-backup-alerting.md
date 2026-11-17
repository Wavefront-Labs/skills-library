---
id: computing-software.systems-network-administration.backup-and-recovery.backup-job-failure-and-missed-backup-alerting
name: backup-job-failure-and-missed-backup-alerting
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [backup-monitoring, backup-reporting, job-failure-alert, missed-backup-alert, dead-mans-switch, healthchecks, rpo-compliance, veeam-one]
level: practitioner
status: draft
description: "Alert on backups that fail and, more importantly, on backups that silently stop: last-success age per workload, dead-man's-switch checks, alert routing and avoiding alert fatigue."
sources:
  - https://helpcenter.veeam.com/docs/one/monitor/about_alarms.html
  - https://healthchecks.io/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Alerting on failed and missed backups

**Goal:** within one backup cycle you know about any workload that is not being protected,
whether the job failed loudly or simply never ran.

## Failure modes to cover
| Mode | Example | Detection |
|---|---|---|
| Job failed | Snapshot error, repository full | Job result alert |
| Job warned | Some VMs skipped, VSS warning | Warning alert, reviewed daily |
| Job never ran | Scheduler disabled, backup server down, licence expired | **Last successful backup age** per workload |
| Workload not in any job | New VM created outside the job's scope | Unprotected workload report |
| Copy/offsite stage failing | Backup copy or cloud tier lagging | Age of the newest offsite restore point |

## The key metric: last-success age
For every protected workload, `now - time of newest successful restore point`, compared to
its RPO. Alert when age > RPO (e.g. > 26 h for daily). This catches every silent failure,
including a dead backup server.

## Implementation options
- Product monitoring: Veeam ONE alarms ("VM with no backups", "backup job state"),
  Commvault/Rubrik SLA reports.
- API-driven check into your monitoring (Prometheus/Zabbix/Nagios): script queries the
  backup server's API for restore points per workload and exports age metrics.
- **Dead-man's switch** for script-based backups (restic, pg_dump cron): the job pings a
  heartbeat URL on success (`curl -fsS https://hc.<domain>/ping/<uuid>`); the monitor alerts
  if no ping arrives within the period. Ping `/fail` on error.
- Email-only alerting from the backup server is not enough: if the server dies, no email.

## Routing and fatigue
- Failures and RPO breaches → on-call ticket/page per severity; warnings → daily review
  queue.
- Retries: alert after the final retry, not every attempt.
- Weekly report: protected vs unprotected workloads, RPO compliance %, failures by cause.

## Verify
Disable a test job (or stop a test restic timer) and confirm an RPO-breach alert fires
within one period; new VMs appear on the unprotected report until added to a job.
