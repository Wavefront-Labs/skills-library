---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-websocket-notifications
name: vaultwarden-websocket-notifications
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, websocket, notifications, reverse-proxy, upgrade-header, enable-websocket]
level: intro
status: docs-checked
description: "Understand Vaultwarden live-sync WebSocket notifications: same port since 1.29, port 3012 removed in 1.31, ENABLE_WEBSOCKET, proxy header needs and verification."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Enabling-WebSocket-notifications"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden WebSocket notifications

Current behaviour: WebSockets run on the main HTTP port and are enabled by default since v1.29.0. Support for the separate port 3012 was removed in v1.31.0, and `WEBSOCKET_ENABLED` and `WEBSOCKET_PORT` are deprecated and ignored. To turn them off set `ENABLE_WEBSOCKET=false` (the saving is modest).

Reverse proxy requirement: the proxy must pass the `Upgrade` and `Connection` headers through to Vaultwarden. Some proxies do so by default (Traefik is the wiki's example); others need explicit configuration, and some wiki proxy examples had not yet been updated for v1.29.0. Old setups that proxied a second `/notifications/hub` location to port 3012 should be simplified to a single upstream.

Verify: in browser developer tools, filter for WebSockets and look for a `101` response on `/notifications/hub`.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Enabling-WebSocket-notifications.
Removed or reworded: the unconfirmed 'two browsers' sync test (the page gives the developer-tools 101 check).
Method: documentation only; no commands were run.
