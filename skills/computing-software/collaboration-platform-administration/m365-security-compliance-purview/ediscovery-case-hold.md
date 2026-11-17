---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.ediscovery-case-hold
name: ediscovery-case-hold
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [ediscovery-case-hold, pv-ediscovery]
level: advanced
status: draft
description: Create a case, place custodians on hold, and search content.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# eDiscovery cases and holds
**Goal:** Create a case, place custodians on hold, and search content.

- Purview > eDiscovery > Standard or Premium > Create case; add members with role group (eDiscovery Manager).
- Add custodians and data sources; create a hold on mailboxes and sites.
- Search with KQL: `from:user@contoso.com AND sent>=2025-01-01`.
- Premium adds review sets, analytics and processing (E5/Premium licence, confirm).

## Gotchas
- Holds can take time to apply; check status before relying on them.
- Roles grant wide data access; scope them with compliance boundaries.

## Self-check
Search statistics show an estimate; the hold status shows On.
