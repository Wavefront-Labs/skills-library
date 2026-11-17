---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.limited-access-sharing-links
name: limited-access-sharing-links
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [limited-access-sharing-links]
level: advanced
status: draft
description: Diagnose the Limited Access and sharing link behaviour.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sharing links and limited access
**Goal:** Diagnose the Limited Access and sharing link behaviour.

- Link types: Anyone, People in your organization, People with existing access, Specific people.
- Limited Access is auto-granted to traverse parent objects; it is not content access.
- Review links via the library 'Manage access' and Graph `permissions`.
- Report oversharing with Data access governance (SharePoint Advanced Management, confirm licence).

## Gotchas
- Cleaning up Limited Access entries manually can break working shares.
- Anyone links bypass identity; restrict them.

## Self-check
Manage access lists links matching the audit expectation.
