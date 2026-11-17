---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.retention-policies-labels
name: retention-policies-labels
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [retention-policies-labels, pv-retention]
level: practitioner
status: draft
description: Retain or delete content with policies, and apply retention labels.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Retention policies and labels
**Goal:** Retain or delete content with policies, and apply retention labels.

- Purview > Data lifecycle management > Retention policies: choose locations and retain/delete period.
- Retention labels apply per item (manually, auto-apply or default label on a library).
- Principle: retention wins over deletion; longest retention wins; explicit label beats implicit policy.
- Preservation lock makes a policy irreversible; use only when required by regulation.

## Gotchas
- Teams chats have a minimum-time-to-delete constraint of about a day (confirm).
- Policies take up to 7 days to be fully effective.

## Self-check
Check the Preservation Hold Library or the item's label after a test deletion.
