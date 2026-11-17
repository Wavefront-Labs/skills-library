---
id: computing-software.rpa-and-low-code.uipath.uipath-queue-items-status
name: uipath-queue-items-status
category: computing-software
field: rpa-and-low-code
product: uipath
tags: [uipath, uipath-orchestrator-queues, uipath-queue-items-status]
level: advanced
status: draft
description: "Use queue transactions with the right status flow."
sources: ['https://docs.uipath.com/', 'https://academy.uipath.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Process queue items and statuses
**Goal:** Use queue transactions with the right status flow.

- Statuses include New, In Progress, Failed, Successful, Abandoned, Retried and Deleted.
- Get Transaction Item sets In Progress; Set Transaction Status closes it; unattended runs that stop leave items Abandoned after a timeout.
- Use Reference and Priority and deadlines to control order.

## Gotchas
- Unique reference options prevent duplicate items; set accordingly.

## Self-check
Items move through the expected statuses.
