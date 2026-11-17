---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.audit-retention-policies
name: audit-retention-policies
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [audit-retention-policies]
level: advanced
status: draft
description: Keep selected audit records longer.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Audit retention policies
**Goal:** Keep selected audit records longer.

- Audit (Premium) > Audit retention policies: filter by activity, user and set duration.
- Default policy retains Exchange, SharePoint, OneDrive and Entra records for a year (confirm).
- Export long-term to a SIEM through the Management Activity API.
- Review cost and licensing.

## Gotchas
- Policy applies to new records going forward, not the past.
- Licence needed per user for extended retention.

## Self-check
A test record has the extended retention in its details.
