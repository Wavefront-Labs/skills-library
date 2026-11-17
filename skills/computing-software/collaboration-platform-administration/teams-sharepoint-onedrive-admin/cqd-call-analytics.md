---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.cqd-call-analytics
name: cqd-call-analytics
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [cqd-call-analytics, tso-call-quality]
level: advanced
status: draft
description: Diagnose call quality using CQD and per-user call analytics.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Call Quality Dashboard and Call analytics
**Goal:** Diagnose call quality using CQD and per-user call analytics.

- Per-user: Teams admin center > Users > user > Meetings & calls > Call analytics.
- Org-wide: CQD (cqd.teams.microsoft.com) with building data upload for subnets.
- Look at jitter, packet loss, round trip and Wi-Fi vs wired.
- Poor stream: ratio of 'poor' streams per building highlights network issues.

## Gotchas
- Without a building file CQD can't segment internal locations.
- Data takes about 24 hours to appear.

## Self-check
CQD shows the building uploaded and the report breaks down by it.
