---
id: computing-software.messaging-and-integration.ntfy.publish-as-json
name: publish-as-json
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, json, publish-json, root-url, fields]
level: practitioner
status: docs-checked
description: "Publish to ntfy with a JSON body POSTed to the root URL, with the full list of supported fields and their defaults."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Publishing as JSON

POST or PUT to the ntfy **root URL** (for example `https://ntfy.sh/`), not the topic URL. This is the most common mistake: a JSON body posted to `/mytopic` is just a message body.

```
curl ntfy.sh -d '{
  "topic": "mytopic",
  "message": "Disk space is low",
  "title": "Low disk space alert",
  "tags": ["warning","cd"],
  "priority": 4
}'
```

## Fields

Only `topic` is required.

- `message`: defaults to `triggered` if empty or missing
- `title`, `tags` (string array), `priority` (integer 1-5, 3 is default)
- `actions` (array of action buttons), `click`, `attach`, `icon`, `filename`
- `markdown` (boolean)
- `delay` (timestamp or duration such as `30min`, `9am`), `timezone`
- `email` (address, or `yes` for your primary verified address)
- `call` (phone number, or `yes`)
- `sequence_id` (for updating and deleting)

## Gotchas

- Limits on title (1 KB) and tags (512 bytes combined) still apply.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Publish as JSON: root URL, field table, topic required, message defaults to triggered). Removed: the Verify step.
Method: documentation only; no commands were run.
