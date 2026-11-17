---
id: computing-software.collaboration-platform-administration.zulip.backup-vs-export-strategy
name: backup-vs-export-strategy
category: computing-software
field: collaboration-platform-administration
product: zulip
tags: [backup-strategy, export-and-import, disaster-recovery, zulip-backup]
level: practitioner
status: docs-checked
description: "Choose between Zulip's backup tool, logical data export, compliance export, HTML archive and replication, including same-version and same-PostgreSQL restore limits."
sources: ["https://zulip.readthedocs.io/en/latest/production/export-and-import.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing a Zulip backup or export tool

Zulip has several tools; pick by purpose.

**Backup tool** (`manage.py backup`): exact restoration of server state for disaster recovery, testing with production data and hardware moves. Highly recommended where applicable because it is fast, robust and least disruptive. Limits: restore on the same Zulip version (precisely, where `manage.py showmigrations` gives identical output) and the same PostgreSQL version; it does not suit moving between self-hosting and Zulip Cloud, which may renumber users and messages. To match PostgreSQL, install with `--postgresql-version`; PostgreSQL can be upgraded independently afterwards.

**Logical data export**: for migrating between Zulip Cloud and other servers, and for audits. It must also be imported on the same Zulip version, but may go to a different PostgreSQL version or a server hosting different organizations. It is disruptive: everyone is logged out and must reset passwords. Output is a `.tar.gz` with JSON files, the same format the Slack and other third-party importers use.

**Compliance exports**: an administrator exports messages matching a search.

**HTML archive tool**: mainly for public archives, but cheap for preserving public channel conversations when decommissioning an organization.

**High availability**: PostgreSQL streaming replication plus the S3 upload backend.

Docker deployments back up the `/data` volume snapshot with a recent database dump rather than routinely using `manage.py backup`, though that command still works for moving between Docker and standard installs in either direction.

The documentation recommends a disaster recovery test after setting up backups, to confirm they work.

## Checked

Method: docs-checked 2026-11-09 against the Zulip Backups, export and import page (read in full); the 'untested backup is only a guess' line replaced with the page's disaster-recovery-test recommendation.
