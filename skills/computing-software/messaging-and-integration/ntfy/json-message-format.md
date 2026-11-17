---
id: computing-software.messaging-and-integration.ntfy.json-message-format
name: json-message-format
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, json, message-format, events, fields]
level: practitioner
status: docs-checked
description: "Reference for the JSON message object ntfy sends to subscribers: fields, event types, and the attachment object."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/subscribe/api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSON message format

Example from the CLI docs:

```
{"id":"nZ8PjH5oox","time":1639971913,"event":"message","topic":"mytopic","message":"hi there"}
```

| Field | Notes |
|---|---|
| `id` | required, random message ID |
| `time` | required, Unix timestamp |
| `expires` | deletion time; not set if `Cache: no` was sent |
| `event` | `open`, `keepalive`, `message`, `message_delete`, `message_clear`, `poll_request` |
| `topic` | comma-separated list in `open` events, single topic otherwise |
| `sequence_id` | used for updating and deleting |
| `message` | always present in `message` events |
| `title` | defaults to `ntfy.sh/<topic>` if unset |
| `tags` | string array |
| `priority` | 1-5 (1 min, 3 default, 5 max) |
| `click` | URL opened on click |
| `actions` | array of action buttons |
| `attachment` | object: `name`, `url`, optional `type`, `size`, `expires` |

## Gotchas

- `type`, `size` and `expires` of an attachment exist only for files uploaded to the ntfy server.
- `message` is only guaranteed in `message` events; the page says you would typically be interested only in `message` events.

## Checked

2026-11-04. Confirmed every field, event type and attachment field against the ntfy subscribe API page (JSON message format tables) and the CLI page example. Removed: the field-order gotcha, the keepalive/open claim and the jq Verify step, none stated on the pages.
Method: documentation only; no commands were run.
