---
id: computing-software.collaboration-platform-administration.mattermost.backup-and-disaster-recovery
name: backup-and-disaster-recovery
category: computing-software
field: collaboration-platform-administration
product: mattermost
tags: [backup, disaster-recovery, active-passive, sso-outage]
level: practitioner
status: docs-checked
description: "Back up a Mattermost server (database, config directory, files), plan active/passive DR, and handle an SSO provider outage."
sources: ["https://docs.mattermost.com/deployment-guide/backup-disaster-recovery.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Backup and disaster recovery

A Mattermost server's state lives in several stores that are backed up and restored separately.

Backup steps:
1. Back up the database with the standard procedure for your database version (for PostgreSQL, an SQL dump).
2. Back up config/config.json. SAML certificate files also live in the config directory, so back up the whole directory.
3. Back up user files: the default ./data directory, a non-default location set by the Directory setting in config.json, or nothing extra if files are in S3 and can stay where they are.

For a clean backup stop Mattermost during the backup, otherwise database and files can fall out of sync. To restore, put the database, config.json and optionally local files back where they were taken from.

Disaster recovery: high availability is a clustered deployment in one site that removes single points of failure; DR covers loss of a whole site. Mattermost supports active/passive DR, where a secondary site stays in sync and is only activated on failover. Active/active, where both sites serve live traffic, is not supported. Automate periodic backups, automate restore or redeploy to cut recovery time, automate verification that backups were produced, and keep copies off-site. Restoring from backup is usually manual and means downtime.

SSO outage (Enterprise): users with a valid session token (30 days by default) keep working; users whose token expires during the outage or who log in on a new device cannot. Mitigate by making the SSO provider highly available, by a custom SAML identity provider fronting an active and a standby option (review its security), or by a manual plan where IT temporarily switches affected accounts from SSO to email-password in the System Console, then switches everyone back afterwards.

## Checked

2026-11-03. Confirmed against the Mattermost documentation page https://docs.mattermost.com/deployment-guide/backup-disaster-recovery. Nothing removed.

Method: documentation only; no commands were run.
