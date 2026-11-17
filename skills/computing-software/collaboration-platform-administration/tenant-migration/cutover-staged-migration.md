---
id: computing-software.collaboration-platform-administration.tenant-migration.cutover-staged-migration
name: cutover-staged-migration
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [cutover-staged-migration, mig-exchange-migrations]
level: practitioner
status: draft
description: Run a migration endpoint and batch.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cutover and staged batches
**Goal:** Run a migration endpoint and batch.

- Create an endpoint (Outlook Anywhere): EAC > Migration > Migration endpoints.
- Create a batch; `New-MigrationBatch -Name Batch1 -SourceEndpoint <ep> -CSVData ([System.IO.File]::ReadAllBytes('users.csv')) -AutoStart`.
- Monitor: `Get-MigrationBatch`, `Get-MigrationUserStatistics -Identity <user> -IncludeReport`.
- Complete the batch and convert on-prem mailboxes to mail users where relevant.

## Gotchas
- Resume failing items with the bad item limit set sensibly.
- Throttling affects speed; avoid peak hours.

## Self-check
Batch status shows Completed with 0 failed users.
