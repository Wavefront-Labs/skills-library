---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.onedrive-sync-known-folder
name: onedrive-sync-known-folder
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [onedrive-sync-known-folder, tso-onedrive]
level: practitioner
status: draft
description: Deploy the OneDrive sync client with KFM and Files On-Demand via policy.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sync client and Known Folder Move
**Goal:** Deploy the OneDrive sync client with KFM and Files On-Demand via policy.

- Policies via ADMX/Intune: `SilentAccountConfig`, `KFMSilentOptIn` (tenant ID), `KFMBlockOptOut`, `FilesOnDemandEnabled`.
- Restrict sync to domain-joined devices: `AllowTenantList` or block personal accounts.
- Check blocked file names and path length limits (400 characters).
- Reset a client: `onedrive.exe /reset`.

## Gotchas
- KFM fails if the user has an existing OneDrive folder duplicates or redirected folders from other tools.
- Policies require the sync app to be current.

## Self-check
Desktop, Documents, Pictures show the cloud icon and appear in the OneDrive web.
