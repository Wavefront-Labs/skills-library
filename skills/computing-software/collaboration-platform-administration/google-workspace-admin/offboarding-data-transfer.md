---
id: computing-software.collaboration-platform-administration.google-workspace-admin.offboarding-data-transfer
name: offboarding-data-transfer
category: computing-software
field: collaboration-platform-administration
product: google-workspace-admin
tags: [offboarding-data-transfer]
level: practitioner
status: draft
description: Offboard a user while keeping Drive, Gmail and calendar data.
sources: ['https://support.google.com/a/', 'https://cloud.google.com/learn/certification/google-workspace-administrator']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Suspend, transfer data and delete
**Goal:** Offboard a user while keeping Drive, Gmail and calendar data.

- Suspend the user first (blocks sign-in, keeps data and licence).
- Transfer ownership: Directory > Users > More options > Transfer data (Drive and Docs, Calendar).
- Use Data Migration or Gmail delegation/forwarding for mail; a shared mailbox via group or delegation.
- Delete only after transfer and any Vault hold; deleted accounts are recoverable for 20 days.

## Gotchas
- Deleting a user without a transfer removes their owned Drive files.
- Licence cost continues for suspended users (some editions), so archive if need be (Archived User licence, confirm).

## Self-check
The manager sees the transferred files in Drive.
