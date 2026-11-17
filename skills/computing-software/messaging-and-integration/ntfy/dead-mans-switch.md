---
id: computing-software.messaging-and-integration.ntfy.dead-mans-switch
name: dead-mans-switch
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, heartbeat, dead-mans-switch, sequence-id, scheduled]
level: advanced
status: docs-checked
description: "Build a heartbeat alert in ntfy by republishing a delayed message to the same sequence ID so it only fires when the sender stops."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/publish.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dead man's switch

Publishing again to the same sequence ID replaces the scheduled message; the original is deleted. So a periodic sender keeps pushing the alert into the future.

```
curl -H "In: 5m" -d "Warning: Server heartbeat stopped!" ntfy.sh/mytopic/heartbeat-check
```

Run that every 60 seconds (cron, systemd timer, loop). If the sender stops, the alert fires 5 minutes after the last run.

## Cancel

```
curl -X DELETE ntfy.sh/mytopic/heartbeat-check
```

or `GET /<topic>/<sequence_id>/delete`. Subscribers see a `message_delete` event.

## Gotchas

- The sequence ID is the last path segment (`/<topic>/<sequence_id>`), or set `X-Sequence-ID`.
- Minimum delay is 10 seconds and maximum is 3 days by default (`message-delay-limit`), which caps the heartbeat window.

## Checked

2026-11-04. Confirmed against the ntfy publish page (Updating and Canceling scheduled notifications, scheduled delivery limits): same-sequence-ID replacement, the 5 minute / 60 second example, DELETE and GET cancel, 10 second minimum and 3 day maximum, `message-delay-limit`, `X-Sequence-ID`. Removed: a caching claim, a CLI claim and the Verify step.
Method: documentation only; no commands were run.
