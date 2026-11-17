---
id: computing-software.cloud-infrastructure-engineering.ansible.controller-database-maintenance-and-pre-upgrade-checks
name: controller-database-maintenance-and-pre-upgrade-checks
category: computing-software
field: cloud-infrastructure-engineering
product: ansible
tags: [ansible, controller-backup-restore, database-maintenance, upgrade-precheck, aap-upgrade]
level: advanced
status: docs-checked
description: "Keep the controller PostgreSQL database healthy (cleanup jobs, vacuum, size monitoring) and run pre-upgrade checks with a tested backup and rollback plan."
sources: ["https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/configuring_automation_execution/", "https://docs.ansible.com/projects/awx/en/latest/rest_api/awx-manage.html", "https://docs.redhat.com/en/documentation/red_hat_ansible_automation_platform/2.5/html-single/rpm_installation/", "https://www.postgresql.org/docs/current/routine-vacuuming.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database maintenance and pre-upgrade checks

## Keep it small
- Management jobs (Administration → Management jobs): **Cleanup Job Details** (default keep 120 days), **Cleanup Activity Stream**, **Cleanup Expired Sessions/OAuth tokens**. Schedule them; reduce retention (e.g. 30-60 days) on busy systems.
- `awx-manage cleanup_jobs` manually (deletes job details/output older than a number of days); job event data is the largest part of the database.
- Lower verbosity and avoid huge registered outputs printed by debug.

## Monitor
```sql
SELECT relname, pg_size_pretty(pg_total_relation_size(relid)) FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 10;
SELECT pg_size_pretty(pg_database_size('awx'));
SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;
```
Autovacuum normally suffices; after big cleanups, `VACUUM (ANALYZE)` affected tables in a quiet window. `VACUUM FULL` locks tables: maintenance window only.

## Pre-upgrade checklist
1. Read release notes and the supported upgrade path (e.g. 2.4 → 2.5 needs specific steps/installer).
2. Check DB version requirements (AAP 2.5 requires PostgreSQL 15).
3. Fresh **backup** (installer backup or AWXBackup CR) and verify it restores in a scratch environment.
4. Record `/api/v2/ping/` versions, instance list, capacity.
5. Export config as code (`awx export > pre-upgrade.json`).
6. Check custom EEs build against the new supported base image; check deprecated settings in `extra_settings`.
7. Drain: disable schedules, wait for running jobs.
8. Upgrade; verify ping, run a smoke job template, re-enable schedules.

## Rollback
No in-place downgrade: rollback = restore the pre-upgrade backup onto the old version.

## Verify
- [ ] Database size trend is flat after cleanup schedules; restore of the latest backup tested this quarter.

## Checked

- 2026-10-31: management jobs (Cleanup Job Details default 120 days running weekly, Cleanup Activity
  Stream, Cleanup Expired Sessions), `awx-manage cleanup_jobs`/`cleanup_activitystream`, `awx-manage
  check_db`, the `/api/v2/ping` health endpoint, database growth guidance and PostgreSQL 15 for AAP 2.5
  confirmed in Configuring automation execution, the AWX awx-manage page, and the RPM installation guide.
  Backup staging (`/var/backups/automation-platform` via `backup_dir`) and the SECRET_KEY file in
  backups confirmed in the installation guides; AWXBackup CR confirmed by the operator's CRD set.
- Removed: the `main_jobevent` partition detail and the 30-60-day retention figure presented as a
  default (retention is configurable per management job).
Method: documentation only; no commands were run.
