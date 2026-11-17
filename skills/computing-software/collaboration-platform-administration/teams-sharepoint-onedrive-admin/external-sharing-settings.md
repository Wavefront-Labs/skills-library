---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.external-sharing-settings
name: external-sharing-settings
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [external-sharing-settings, tso-sharepoint-sharing]
level: practitioner
status: draft
description: Set the tenant sharing ceiling and tighter per-site levels.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tenant and site sharing levels
**Goal:** Set the tenant sharing ceiling and tighter per-site levels.

- SharePoint admin center > Policies > Sharing: Anyone, New and existing guests, Existing guests, Only people in your org.
- Per site: `Set-SPOSite -Identity <url> -SharingCapability ExistingExternalUserSharingOnly`.
- Domain allow/deny lists and link expiration for Anyone links.
- Set default link type to Specific people.

## Gotchas
- Site setting can never exceed tenant setting.
- OneDrive sharing can be stricter than SharePoint.

## Self-check
A test external recipient is denied or allowed as designed.
