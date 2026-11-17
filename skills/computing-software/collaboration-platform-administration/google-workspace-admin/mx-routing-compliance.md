---
id: computing-software.collaboration-platform-administration.google-workspace-admin.mx-routing-compliance
name: mx-routing-compliance
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [mx-routing-compliance, gws-gmail-mail-flow]
level: practitioner
status: draft
description: Set MX records and Gmail routing/compliance settings.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MX, routing and compliance rules
**Goal:** Set MX records and Gmail routing/compliance settings.

- MX: smtp.google.com priority 1 (current single-record guidance, confirm) or the legacy ASPMX set with priorities.
- Apps > Google Workspace > Gmail > Routing: dual delivery, split delivery, recipient address map.
- Compliance: content compliance, attachment compliance, objectionable content, append footer.
- Inbound gateway setting lists trusted third-party filter IPs.

## Gotchas
- Apply routing to correct OU or message direction to avoid loops.
- Allow time for MX TTL after a change.

## Self-check
Send a test message and view original headers for the expected path.
