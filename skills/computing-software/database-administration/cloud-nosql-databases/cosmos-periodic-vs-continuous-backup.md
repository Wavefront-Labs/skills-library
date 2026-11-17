---
id: computing-software.database-administration.cloud-nosql-databases.cosmos-periodic-vs-continuous-backup
name: cosmos-periodic-vs-continuous-backup
category: computing-software
field: database-administration
product: cloud-nosql-databases
tags: [cosmos-periodic-vs-continuous-backup, cosmos-backup, cosmos-db, azure-cosmos-db, cloud-nosql-databases, database-administration]
level: practitioner
status: docs-checked
description: "Choose a backup mode that meets your recovery objectives."
sources:
  - https://learn.microsoft.com/en-us/azure/cosmos-db/online-backup-and-restore
  - https://learn.microsoft.com/en-us/azure/cosmos-db/periodic-backup-restore-introduction
  - https://learn.microsoft.com/en-us/azure/cosmos-db/continuous-backup-restore-introduction
  - https://learn.microsoft.com/en-us/cli/azure/cosmosdb
  - https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Periodic versus continuous backup

**Goal:** Choose a backup mode that meets your recovery objectives.

## Steps
- Periodic (default): a full backup every 4 hours, with the latest two kept by default (interval and retention can be changed in the portal); restore is requested through a support request.
- Continuous (7, 30 or 35 day tier): point-in-time restore, self-service through the portal, PowerShell or CLI: az cosmosdb restore -g RG --target-database-account-name NEW --account-name OLD --restore-timestamp 2026-11-01T10:00:00Z --location westeurope
- Migrate periodic to continuous with az cosmosdb update --backup-policy-type Continuous.
- An account restore always creates a new account.

## Gotcha
An account in continuous mode cannot be switched back to periodic.

## Checked

2026-11-03. Confirmed against the online backup, periodic backup and continuous backup pages and the az cosmosdb restore and update references (restore needs -g, --target-database-account-name, --account-name, --restore-timestamp, --location; update --backup-policy-type accepts Continuous or Periodic): periodic default, 4-hour interval, two copies, support-request restore, 7/30/35-day tiers, migrate periodic to continuous, no switch back, restore into a new account.
Removed: the 8 hour retention figure (derived, not stated) and "any second" (not stated). Added the missing -g to the restore command.
Method: documentation only; no commands were run.

## Verify
- [ ] A test restore into a new account returns the expected data at the timestamp.
