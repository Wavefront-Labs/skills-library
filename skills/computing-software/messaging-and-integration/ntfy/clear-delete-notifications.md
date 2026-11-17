---
id: computing-software.messaging-and-integration.ntfy.clear-delete-notifications
name: clear-delete-notifications
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, clear, delete, message-clear, message-delete]
level: practitioner
status: docs-checked
description: "Mark ntfy notifications read or delete them by sequence ID, and what message_clear and message_delete events subscribers see."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clearing and deleting

## Clear (mark as read, dismiss)

```
curl -X PUT ntfy.sh/mytopic/backup-42/clear
```

Alias path `/read`. `GET /<topic>/<sequence_id>/clear` (or `/read`) also works for limited clients. Emits a `message_clear` event.

## Delete (remove from drawer and client database)

```
curl -X DELETE ntfy.sh/mytopic/backup-42
```

`GET /<topic>/<sequence_id>/delete` works for limited clients. Emits a `message_delete` event.

## Gotchas

- Deleted sequences can be revived by publishing again with the same sequence ID.
- Deleting a scheduled message before delivery removes it from the server so it is never delivered.
- The `message_clear` and `message_delete` events are used by the web and Android apps to update the notification.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Clearing and Deleting notifications, scheduled delivery): PUT clear, read alias, DELETE, GET fallbacks, event names, revival by same sequence ID, scheduled-message deletion. Removed: a CLI claim, a client-behaviour claim and the Verify step.
Method: documentation only; no commands were run.
