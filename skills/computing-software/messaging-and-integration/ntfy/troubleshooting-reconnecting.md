---
id: computing-software.messaging-and-integration.ntfy.troubleshooting-reconnecting
name: troubleshooting-reconnecting
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, reconnecting, late-notifications, websocket, http-403]
level: practitioner
status: docs-checked
description: "Fix ntfy clients stuck on Reconnecting or receiving notifications 30+ minutes late on a self-hosted server."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/troubleshooting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# "Reconnecting..." and late notifications

Symptoms: all topics show "Reconnecting...", notifications arrive 30+ minutes late, or new pushes appear only after a manual refresh.

## Checklist

1. Reverse proxy: set `behind-proxy: true` in ntfy, and enable WebSockets in the proxy (see behind-proxy).
2. Permissions: every subscribed topic must be accessible to a logged-in user or `everyone`. All topics share one WebSocket/JSON request, so one topic returning `403 Forbidden` blocks the whole request.
3. UnifiedPush: make sure `everyone` can write to `up*` and your user can read `up*`.

## Further debugging

The page's general advice is to enable `log-level: debug` or `trace` on the server (see the troubleshooting-debug skill).

## Checked

2026-11-04. Confirmed against the ntfy troubleshooting page (Reconnecting / late notifications checklist: behind-proxy, WebSockets, 403 blocks the joined request, up* permissions). Removed: the invented curl diagnosis, the Android warning-icon list and the Verify step.
Method: documentation only; no commands were run.
