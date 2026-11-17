---
id: computing-software.collaboration-platform-administration.tenant-migration.domain-move-cross-tenant-onedrive
name: domain-move-cross-tenant-onedrive
category: computing-software
field: collaboration-platform-administration
product: tenant-migration
tags: [domain-move-cross-tenant-onedrive]
level: advanced
status: draft
description: Move custom domains and OneDrive content between tenants.
sources: ['https://learn.microsoft.com/en-us/exchange/mailbox-migration/mailbox-migration', 'https://learn.microsoft.com/en-us/sharepointmigration/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Domain transfer and cross-tenant OneDrive
**Goal:** Move custom domains and OneDrive content between tenants.

- Remove the domain from users, groups, and aliases in the source tenant before verifying it in the target.
- Cross-tenant OneDrive migration with `Start-SPOCrossTenantUserContentMove` (SharePoint Online Management Shell; confirm module version and prerequisites).
- Third-party tools cover Teams and SharePoint content that Microsoft tools do not.
- Plan guest/external user access and shared link breakage.

## Gotchas
- Domain removal commonly fails because of lingering references; use the admin center's removal assistance.
- Teams chats are not natively moved.

## Self-check
The domain shows verified in the target and test users keep their OneDrive content.
