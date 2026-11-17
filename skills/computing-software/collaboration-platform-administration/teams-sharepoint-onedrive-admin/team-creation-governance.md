---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.team-creation-governance
name: team-creation-governance
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [team-creation-governance, tso-team-lifecycle]
level: advanced
status: draft
description: Control who creates Microsoft 365 groups and enforce naming and expiration.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Restrict creation, naming and expiration
**Goal:** Control who creates Microsoft 365 groups and enforce naming and expiration.

- Restrict creation: Entra group setting `EnableGroupCreation=false` with `GroupCreationAllowedGroupId` of a security group.
- Naming policy: prefix/suffix and blocked words in Entra Groups > Naming policy (licence needed, confirm).
- Expiration policy: Entra Groups > Expiration (e.g. 365 days) with owner renewal.
- Provide a request workflow so restriction doesn't drive shadow IT.

## Gotchas
- Group creation restriction also affects Planner, Yammer/Viva Engage and others.
- Expiry deletes the group, including the site and mailbox (restorable within 30 days).

## Self-check
A non-allowed user cannot create a team; an allowed user can.
