---
id: computing-software.messaging-and-integration.ntfy.update-notifications
name: update-notifications
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, sequence-id, update, x-sequence-id, replace]
level: practitioner
status: docs-checked
description: "Update an existing ntfy notification by publishing again with the same sequence ID, via path, header, query or JSON."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Updating notifications with sequence IDs

Notifications are linked by a sequence ID. The server is append-only: existing messages are never changed; a new message carries the update and clients replace the old one.

## Set the sequence ID

- Use the `id` returned from the first publish as the sequence ID, or choose your own.
- Path: `POST /<topic>/<sequence_id>`
- Header on `POST /<topic>`: `X-Sequence-ID` (aliases `Sequence-ID`, `SID`)
- Query parameter `sequence-id`, JSON field `sequence_id`, or the CLI flag `--sequence-id`.

```
curl -d "Backup running" ntfy.sh/mytopic/backup-42
curl -d "Backup done" ntfy.sh/mytopic/backup-42
```

If `id` and `sequence_id` differ, the response includes `sequence_id`.

## Related actions

Clearing and deleting use the same sequence ID; see the clear-delete-notifications skill. Republishing to a sequence ID is also how the dead man's switch pattern replaces a scheduled message.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Updating + deleting notifications: sequence ID forms, append-only behaviour, sequence_id in responses, scheduled replacement). Added: CLI flag. Removed: the Verify step.
Method: documentation only; no commands were run.
