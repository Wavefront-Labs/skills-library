---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.permission-levels-groups
name: permission-levels-groups
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [permission-levels-groups, tso-sharepoint-permissions]
level: practitioner
status: draft
description: Apply permission groups and manage inheritance.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Groups, permission levels and inheritance
**Goal:** Apply permission groups and manage inheritance.

- Default groups: Owners (Full Control), Members (Edit), Visitors (Read).
- Prefer Microsoft 365 group membership to site-level groups for team sites.
- Break inheritance rarely; use a check permissions report.
- Site collection admins via `Set-SPOUser -Site <url> -LoginName <upn> -IsSiteCollectionAdmin $true`.

## Gotchas
- Unique permissions over 50,000 per list slow the system; stay far under.
- Everyone except external users group is broad; avoid in sensitive sites.

## Self-check
Check Permissions on a sample file returns the expected principals.
