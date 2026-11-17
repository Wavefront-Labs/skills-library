---
id: computing-software.database-administration.sql-server.azure-sql-automated-backups-and-ltr
name: azure-sql-automated-backups-and-ltr
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, azure-sql-database, azure-sql-managed-instance, long-term-retention, azure-sql-pitr, geo-restore, deleted-database-restore]
level: practitioner
status: docs-checked
description: "Use Azure SQL automated backups: PITR retention, long-term retention policies, geo-restore, restoring deleted databases, and backup storage redundancy."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/automated-backups-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/long-term-retention-overview
  - https://learn.microsoft.com/en-us/azure/azure-sql/database/recovery-using-backups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure SQL automated backups, PITR and LTR

Azure SQL Database and Managed Instance take full, differential (12 or 24 h) and log
(about every 10 min) backups automatically.

## Point-in-time restore (PITR)
Retention 1-35 days (default 7; Basic tier max 7). Restore always creates a **new database**:
```bash
az sql db show -g rg -s sql-prod -n sales --query earliestRestoreDate
az sql db restore -g rg -s sql-prod -n sales --dest-name sales_0830 --time "2026-10-18T08:30:00Z"
az sql db str-policy set -g rg -s sql-prod -n sales --retention-days 14 --diffbackup-hours 12
```
Then rename (`ALTER DATABASE sales MODIFY NAME = sales_old` and swap) or copy rows back.
Restore time depends on database size and log volume; test it to know your real RTO.

## Long-term retention (LTR)
Keeps weekly/monthly/yearly full backups up to 10 years in Azure Blob Storage:
```bash
az sql db ltr-policy set -g rg -s sql-prod -n sales \
  --weekly-retention P8W --monthly-retention P12M --yearly-retention P7Y --week-of-year 1
az sql db ltr-backup list -l westeurope -s sql-prod -d sales -o table
az sql db ltr-backup restore --backup-id "<id>" --dest-database sales_2025 --dest-server sql-prod --dest-resource-group rg
```
In SQL Database (not Managed Instance) LTR backups can be configured as immutable.

## Geo-restore
With geo-redundant backup storage, restore to any region from the latest geo-replicated
backup: `az sql db geo-backup restore` / portal "Geo-restore".
For low RPO/RTO use active geo-replication or failover groups.

## Deleted database
Restorable until the PITR retention ends (if the server still exists):
`az sql db list-deleted -g rg -s sql-prod`, then restore with `--deleted-time`.

## Backup storage redundancy
Locally redundant (LRS), zone-redundant (ZRS), geo-redundant (RA-GRS, the default) and
geo-zone-redundant (GZRS). Data residency rules may require keeping backups in-region.

## Gotchas
- PITR to a point before a schema change restores the old schema; plan application compatibility.
- Backup storage beyond the free amount (equal to the database max data size) is billed.

## Verify
Quarterly restore drill: PITR to a new name, run integrity and row-count checks, record the
elapsed time against RTO; `az sql db ltr-backup list` shows the expected weekly/monthly entries.

## Checked
2026-10-28. Confirmed against the automated-backups-overview, long-term-retention-overview and recovery-using-backups pages: PITR retention 1-35 days (7 default, Basic 1-7), differential every 12 or 24 hours, log backups about every 10 minutes, LTR up to 10 years, LTR immutability supported in SQL Database but not Managed Instance, default geo-redundant backup storage, restore creates a new database, deleted-database restore on the same server within retention. The az commands passed check_commands.
Removed unconfirmed claims: weekly full cadence of automated backups, native BACKUP limits and COPY_ONLY on Managed Instance, "RA-GRS" for LTR, LTR surviving server deletion, geo-restore RPO of 1 hour, "cheapest DR option", server deletion removing PITR backups, TDE customer-managed key note.
Method: documentation only; no commands were run.
