---
id: computing-software.networking-hardware-and-wireless.asterisk.ari-outbound-websockets
name: ari-outbound-websockets
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ari, outbound-websocket, websocket-client-conf, persistent, per-call, reconnect, stasis]
level: advanced
status: docs-checked
description: "Configure Asterisk to connect out to ARI applications using outbound_websocket in ari.conf plus websocket_client.conf, persistent versus per-call, reload behaviour and CLI checks."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/ARI-Outbound-Websockets/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARI outbound websockets
Asterisk can connect to an external ARI application rather than waiting for one. Two types:
- **Persistent**: opened at startup, kept open, reconnects at a configurable interval.
- **Per-call**: a template that connects only when `Stasis()` runs with a matching app, and disconnects when it returns. Reconnection attempts are limited by `reconnect_attempts`; on failure `${STASISSTATUS}` is `FAILED` and dialplan continues.

`ari.conf` section: `type=outbound_websocket`, `websocket_client_id` (a section in `websocket_client.conf`), `apps` (comma list; one app may belong to only one connection), `subscribe_all` (default no), `local_ari_user` (a local user with a plain-text password; sets read-only or read/write).

`websocket_client.conf` (shared with the WebSocket channel driver) sets `uri`, `protocols = ari`, `username`, `password`, `connection_type`, `connection_timeout`, `reconnect_interval`, `reconnect_attempts`, `tls_enabled`, `verify_server_cert`, `verify_server_hostname`.

Reloads: `module reload res_ari.so` also reloads `websocket_client.conf`. Changing `apps` is safe; moving an app between connections takes two reloads. Changing other parameters reconnects. Duplicate apps or a missing `local_ari_user` mark the connection invalid.

CLI: `ari show outbound-websockets`, `ari show outbound-websocket <connection_id>`.

For extra channels on a per-call connection, give `app` as `<app name>:<channel name>`.

## Checked

2026-11-09. Confirmed against the Asterisk ARI Outbound Websockets page: persistent and per-call types, ari.conf parameters and defaults, websocket_client.conf parameters from the sample, reload behaviour, invalid-connection conditions, STASISSTATUS FAILED, app name format for extra channels and the two ari show commands. The page describes the feature as arriving in upcoming releases; the skill makes no version claim. Nothing changed.
Method: documentation only; no commands were run.
