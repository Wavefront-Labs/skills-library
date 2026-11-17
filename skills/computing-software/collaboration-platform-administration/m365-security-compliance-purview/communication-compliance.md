---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.communication-compliance
name: communication-compliance
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [communication-compliance]
level: advanced
status: draft
description: Detect policy-violating communications.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Communication compliance
**Goal:** Detect policy-violating communications.

- Create a policy: choose users, locations (Exchange, Teams, Viva Engage), conditions (classifiers, keywords).
- Set reviewers and remediation (escalate, resolve, notify).
- Sample percentage lowers review load.
- Use a scoped admin group.

## Gotchas
- Works on new communications after enabling.
- Keep reviewers small and trained.

## Self-check
A test message with a trigger term appears in pending review.
