---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.custom-app-upload
name: custom-app-upload
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [custom-app-upload]
level: advanced
status: draft
description: Control sideloading and publish line-of-business apps.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Custom apps and uploads
**Goal:** Control sideloading and publish line-of-business apps.

- Upload policy: Setup policies > allow user to upload custom apps (avoid for most users).
- Publish an app package (manifest.json + icons zip) via Manage apps > Upload new app.
- Review app permissions and RSC consent before approval.
- Use Graph for governance of installed apps.

## Gotchas
- Sideloading is risky; allow it only for dev groups.
- Manifest schema version must be supported.

## Self-check
The app shows in the org store and installs for a test user.
