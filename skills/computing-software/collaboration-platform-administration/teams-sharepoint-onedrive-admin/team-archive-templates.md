---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.team-archive-templates
name: team-archive-templates
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [team-archive-templates]
level: practitioner
status: draft
description: Archive inactive teams and use templates for consistent structure.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Archive and templates
**Goal:** Archive inactive teams and use templates for consistent structure.

- Teams admin center > Teams > Manage teams > Archive; archiving makes the team read-only and sets its site read-only (optional).
- Team templates: Teams > Team templates; or Graph `POST /teams` with `template@odata.bind`.
- Review ownerless teams monthly: Entra group owners report or Graph.
- Delete is soft for 30 days, restore with `Restore-MgDirectoryDeletedItem`.

## Gotchas
- Archived teams still consume storage.
- Templates cannot be applied to existing teams.

## Self-check
An archived team shows read-only state and a new team from the template matches it.
