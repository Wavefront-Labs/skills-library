---
id: computing-software.networking-hardware-and-wireless.asterisk.ari-configuration-and-getting-started
name: ari-configuration-and-getting-started
category: computing-software
field: networking-hardware-and-wireless
product: asterisk
tags: [networking-hardware-and-wireless, asterisk, ari, rest-interface, http-conf, ari-conf, stasis, websocket, swagger]
level: practitioner
status: docs-checked
description: "Enable ARI in http.conf and ari.conf, define users, connect a WebSocket to /ari/events with an app name, and hand channels over with Stasis."
sources:
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/Asterisk-Configuration-for-ARI/
  - https://docs.asterisk.org/Configuration/Interfaces/Asterisk-REST-Interface-ARI/Getting-Started-with-ARI/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ARI configuration and getting started
ARI is served by Asterisk's built-in HTTP server, so both `http.conf` and `ari.conf` matter.

`http.conf`: `enabled=yes`, `bindaddr`, `bindport` (default 8088). For TLS add `tlsenable`, `tlsbindaddr`, `tlscertfile`, `tlsprivatekey`; the docs recommend TLS/WSS.

`ari.conf`:
- `[general]` holds `enabled` and `pretty` (pretty-printed JSON).
- Each user is a section with `type=user`, `password`, and `read_only` (a read-only user cannot make changing requests).

Applications connect a WebSocket to `/ari/events` with `app=<name>` and credentials (for example `api_key=user:pass`). The Stasis app name is the handle for everything that app controls.

Handing over a channel from the dialplan:
```
exten => 1000,1,NoOp()
 same => n,Answer()
 same => n,Stasis(channel-dump)
 same => n,Hangup()
```
The channel is controlled over REST until it leaves Stasis, then dialplan resumes. The REST API is documented with Swagger, which also generates interactive documentation (Swagger-UI).

Credentials such as `asterisk`/`asterisk` in examples must not be used in production.

## Checked
2026-11-09: read the Asterisk Configuration for ARI and Getting Started with ARI pages in full and confirmed the http.conf and ari.conf options and defaults, the Stasis application, the /ari/events WebSocket with app and api_key, and the demo-credentials warning. Removed the reference to a Using Swagger page (not in the cited pages) and replaced it with the Swagger statement the Getting Started page makes.

Method: documentation only; no commands were run.
