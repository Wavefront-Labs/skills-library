---
id: computing-software.collaboration-platform-administration.tenant-migration.sharepoint-migration-tool
name: sharepoint-migration-tool
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [sharepoint-migration-tool, mig-files-sharepoint]
level: practitioner
status: draft
description: Move file shares and SharePoint Server content with SPMT.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SharePoint Migration Tool
**Goal:** Move file shares and SharePoint Server content with SPMT.

- Install SPMT, sign in, choose source (file share or SharePoint Server), then destination.
- Use a CSV or JSON for bulk with source path, target site, library.
- Preserve permissions and metadata options; use incremental runs.
- Reports show skipped and failed items.

## Gotchas
- Invalid characters and long paths fail; fix names first.
- Throttling shapes speed; use Azure-assisted mode via the tool.

## Self-check
Final report shows zero failures or documented exceptions.
