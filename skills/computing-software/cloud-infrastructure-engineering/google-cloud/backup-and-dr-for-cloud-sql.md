---
id: computing-software.cloud-infrastructure-engineering.google-cloud.backup-and-dr-for-cloud-sql
name: backup-and-dr-for-cloud-sql
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, backup-and-dr, backup-dr-cloud-sql, backup-vaults, cloud-sql, immutable-backups, enhanced-backups]
level: practitioner
status: docs-checked
description: "Protect Cloud SQL with Backup and DR Service backup plans in backup vaults: vault creation, enforced retention, backup rules, regions and restore."
sources: ["https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-vault", "https://cloud.google.com/sdk/gcloud/reference/backup-dr/backup-plans/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup and DR for Cloud SQL

Cloud SQL instances can be protected by Backup and DR Service, which stores backups in a **backup
vault**: a Google-managed regional resource with isolated, immutable and indelible storage. Enforced
retention means backups cannot be deleted by anyone until the period passes, which protects against
accidental or malicious deletion.

## Setup
1. Backup vault, in a dedicated backup project (the vault page describes project-level identity isolation):
   ```bash
   gcloud backup-dr backup-vaults create sql-vault --location=europe-west2 \
     --backup-min-enforced-retention=30d --project=<BACKUP_P>
   ```
   The minimum enforced retention can be set from 1 day to 99 years; a backup plan using the vault must have retention equal to or longer than it.
2. Backup plan with a schedule and retention (rule syntax from the gcloud reference):
   ```bash
   gcloud backup-dr backup-plans create sql-daily --location=europe-west2 \
     --resource-type=<RESOURCE_TYPE> \
     --backup-vault=projects/<BACKUP_P>/locations/europe-west2/backupVaults/sql-vault \
     --backup-rule="rule-id=daily,retention-days=35,recurrence=DAILY,backup-window-start=2,backup-window-end=6" \
     --project=<BACKUP_P>
   ```
   Take the `RESOURCE_TYPE` value for Cloud SQL from the Backup and DR Cloud SQL documentation, and check `gcloud backup-dr backup-plans create --help`.
3. Associate the plan with the instance through the Google Cloud console, which is the documented path for Cloud SQL.

## Notes
- Cloud SQL is a console-managed workload for backup vaults.
- Region: backup plans in the console must be created in the same region as the source workload. The vault page has a table of regional, multi-regional and cross-regional vault support per workload; check it for Cloud SQL.
- Lock the enforced retention period for strict compliance: after the effective date no one, not even a Project Owner, can decrease it, only increase it.
- Backups under enforced retention still incur storage charges for the full period.

## Verify
- [ ] First vault backup appears; a test restore to a new instance succeeds and data matches.

## Checked
2026-10-31. Confirmed against the backup vault concepts page (regional Google-managed resource, immutable and indelible, enforced retention 1 day to 99 years, plan retention at least the vault minimum, lock behaviour, same-region rule for console backup plans, storage charges) and the `gcloud backup-dr backup-plans create` reference (flags and backup-rule syntax). Removed unconfirmed claims: the Cloud SQL resource type string, hourly-frequency in a daily rule, restore and PITR behaviour, IAM role names, and the claims about standard backup deletion and enhanced-backup side effects. The Cloud SQL-specific Backup and DR pages cited earlier returned 404.
Method: documentation only; no commands were run.
