---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.access-policies-labels-sites
name: access-policies-labels-sites
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [access-policies-labels-sites]
level: advanced
status: draft
description: Apply container labels and limit access from unmanaged devices.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sensitivity labels and unmanaged device policy
**Goal:** Apply container labels and limit access from unmanaged devices.

- Policies > Access control > Unmanaged devices: full, limited web-only, or block.
- Requires Conditional Access integration with Entra (reference).
- Sensitivity labels with container settings govern privacy and external sharing of a site.
- `Set-SPOSite -ConditionalAccessPolicy AllowLimitedAccess`.

## Gotchas
- Limited access disables sync and desktop edit from unmanaged devices.
- Labels for containers must be enabled with `Set-SPOTenant`-related steps in Purview.

## Self-check
Unmanaged-browser session shows the limited banner.
