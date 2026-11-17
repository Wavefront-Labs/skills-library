---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-backup-and-restore
name: app-service-backup-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service, webapp-backup, webapp-restore, automatic-backups, custom-backups, disaster-recovery]
level: practitioner
status: docs-checked
description: "Back up and restore App Service apps: automatic vs custom backups, storage and database inclusion, restore to another app or slot, and limits that catch people out."
sources: ["https://learn.microsoft.com/en-us/azure/app-service/manage-backup", "https://learn.microsoft.com/en-us/cli/azure/webapp/config/backup", "https://learn.microsoft.com/en-us/cli/azure/webapp/config/snapshot"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service backup and restore

**Goal:** recover an app's content and configuration after a bad deployment or deletion - and know what isn't covered.

## Automatic backups
- On Basic, Standard, Premium and Isolated tiers App Service takes automatic backups (hourly, not configurable; retention 30 days, not configurable: hourly for days 1-3, every third hourly backup for days 4-14, every sixth for days 15-30; up to 30 GB) of app content and
  configuration - no storage account needed, linked databases are not backed up, and they are not downloadable or available over a virtual network. On Basic only the production slot can be backed up and restored.
```bash
az webapp config snapshot list -g rg -n app-orders -o table
az webapp config snapshot restore -g rg -n app-orders --time "2026-10-17T22:00:00"   # overwrites the app's content and configuration
az webapp config snapshot restore -g rg -n app-orders-restore --source-name app-orders --time "2026-10-17T22:00:00"   # restore into a different app
```

## Custom backups (Basic, Standard, Premium, Isolated)
- To your storage account container, on demand or on a schedule (every 2 hours at minimum, up to 12 backups per day; retention 0-30 days or indefinite), with partial backups supported. The storage account must support SAS-based authorization; managed identity authentication to the storage account is not supported.
- Linked databases (SQL Database, Azure Database for MySQL and PostgreSQL Single Server, MySQL in-app) can be included, but **starting 3/31/2028 custom backups no longer support backing up linked databases**; Flexible Server options are not supported, and a backup over a virtual network cannot include linked databases.
```bash
# <container-url-with-sas>: URL of the backup container including a SAS token
az webapp config backup update -g rg --webapp-name app-orders \
  --container-url "<container-url-with-sas>" \
  --frequency 1d --retain-one true --retention 30
az webapp config backup create -g rg --webapp-name app-orders --container-url "<url-with-sas>" --backup-name pre-release
az webapp config backup list -g rg --webapp-name app-orders -o table
az webapp config backup restore -g rg --webapp-name app-orders --container-url "<url-with-sas>" \
  --backup-name pre-release --overwrite
```

## Limits and coverage
- Custom backups are limited to 10 GB, of which 4 GB can be the linked database; exclude folders with a `_backup.filter` file in `wwwroot` and back up databases with their native tools.
- Not covered: content from custom-mounted Azure storage (for example Azure Files). Restoring app configuration does not restore network features, authentication, managed identities, custom domains, TLS/SSL, scale out, alerts, backup settings or deployment slots.
- Firewall-protected storage account: custom backups work over a virtual network when the app is VNet integrated (or in an App Service Environment v3) and the storage account allows that network.
- App Service stops the target app or slot while restoring; restore to a deployment slot first, then swap, to limit downtime. Restoring into an existing slot erases and overwrites its file system.

## Better practice
For code, the deployment pipeline is the real backup (redeploy a known artifact). Use backups for content-heavy
apps (CMS uploads) and as a safety net; databases rely on their own point-in-time restore.

## Verify
- [ ] Test restore into a separate app/slot succeeds and the site renders; backup list shows recent successful runs.
- [ ] Automatic backups are stored in the same datacenter as the app, so they are not a disaster recovery plan.

## Checked
Checked 2026-10-24 against azure-docs app-service manage-backup and the azure-docs-cli webapp config backup and snapshot references (flags --container-url, --frequency, --retain-one, --retention, --backup-name, --overwrite, --target-name for backup; --time, --source-name, --restore-content-only for snapshot). Confirmed: automatic versus custom comparison (tiers, 30 GB and 10 GB sizes, hourly and 2-hour minimum frequency, retention rules, no linked databases in automatic backups), SAS-only storage authentication, backup over a virtual network, _backup.filter, restored and non-restored settings, az webapp config snapshot list and restore for automatic backups. Found wrong and fixed: custom backups were stated as Standard and above (Basic and above), snapshot restore was shown with --target-name and --overwrite which it does not accept, the linked database feature was presented without the 3/31/2028 end of support, the user delegation SAS example was not documented. Removed unconfirmed: the Key Vault reference note.

Method: documentation only; no commands were run.
