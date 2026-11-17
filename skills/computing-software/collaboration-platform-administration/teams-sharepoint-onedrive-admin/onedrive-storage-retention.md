---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.onedrive-storage-retention
name: onedrive-storage-retention
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [onedrive-storage-retention]
level: practitioner
status: draft
description: Set quotas and the retention of deleted users' OneDrive.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storage quota and departed-user retention
**Goal:** Set quotas and the retention of deleted users' OneDrive.

- Default 1 TB per user, expandable to 5 TB by request in many plans (confirm).
- SharePoint admin center > Settings > OneDrive retention: days after user deletion (default 30, max 3650).
- `Set-SPOTenant -OrphanedPersonalSitesRetentionPeriod 120`.
- Give the manager access to the files before the retention ends.

## Gotchas
- Without access granted, content is deleted after the period.
- Retention policies in Purview can extend retention.

## Self-check
Deleted-user OneDrive is accessible by the manager during the period.
