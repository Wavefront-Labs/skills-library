---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.grafana-upgrade-procedure
name: grafana-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [grafana-upgrade-procedure, grafana-upgrade, grafana-backup, grafana-plugins, database-migrations]
level: practitioner
status: docs-checked
description: "Upgrade self-hosted Grafana safely: read the version guides and What's new, back up config, plugins and the database (SQLite, MySQL, Postgres), and keep the backup for rollback."
sources: ["https://grafana.com/docs/grafana/latest/upgrade-guide/", "https://grafana.com/docs/grafana/latest/whatsnew/", "https://grafana.com/docs/grafana/latest/administration/back-up-grafana/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grafana upgrade procedure

## Before
1. Read the upgrade guide for the version you are moving to (the index lists guides for v11, v12 and v13, plus "Upgrade strategies"; guides for v10.4 and earlier are in the documentation archive) and the What's new page of each release you cross for highlights, deprecations and breaking changes. Grafana says you can upgrade to any supported release from any supported release, and that upgrades are backward compatible so dashboards and graphs will not change; it recommends upgrading often.
2. Back up (from the Back up Grafana page):
   - Configuration: copy the config files you modified. `defaults.ini` is the default (do not change it) and `custom.ini` the custom file; for deb or rpm installs the config is `/etc/grafana/grafana.ini`.
   - Plugin data: copy the plugin folders recursively. Default location is `$WORKING_DIR/data/plugins` for binary or source installs and `/var/lib/grafana/plugins` for deb or rpm packages.
   - Database, so you can roll back to a previous version:
     - SQLite (the default) is a single file: `$WORKING_DIR/data/grafana.db`, or `/var/lib/grafana/grafana.db` for deb or rpm. Shut Grafana down before copying it, for data integrity.
     - MySQL: `mysqldump -u root -p[root_password] [grafana] > grafana_backup.sql`, restore with `mysql -u root -p grafana < grafana_backup.sql`.
     - Postgres: `pg_dump grafana > grafana_backup`, restore with `psql grafana < grafana_backup`.
3. Try the upgrade in a non-production copy restored from that backup first.

## Rollback
The documented way to return to a previous version is the database backup taken before the upgrade, together with the matching configuration and plugin backups. Keep the backup until you are satisfied with the new version.

## Checked
Date: 2026-11-07.
Read in full: Upgrade Grafana (the index page), Back up Grafana, and the What's new index. The old `breaking-changes` URL now redirects to the What's new index, so the source was replaced with the `whatsnew` URL; the per-version upgrade guides and What's new pages themselves were not read, so version-specific changes are deliberately not claimed.
Removed because no cited page confirms them: the Angular plugin removal and alerting migration claims, the `/api/plugins` inventory call, provisioning directory backup, Docker, Helm and apt upgrade steps, the automatic-migration and log-message claims, alerting API and metric checks, the claim that downgrading a migrated database is unsupported, the feature toggle gotcha, the warning about skipping many majors (the upgrade guide says any supported release to any supported release), and the invented Verify checklist.
Method: documentation only; no commands were run.
