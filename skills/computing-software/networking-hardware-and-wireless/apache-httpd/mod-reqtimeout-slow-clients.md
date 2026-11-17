---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-reqtimeout-slow-clients
name: mod-reqtimeout-slow-clients
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-reqtimeout, requestreadtimeout, slowloris, timeouts, 408]
level: practitioner
status: docs-checked
description: "Defend against slow clients with RequestReadTimeout: handshake, header and body timeouts, MinRate extension, the default value and per-vhost disabling."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html
  - https://httpd.apache.org/docs/2.4/misc/security_tips.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_reqtimeout
`RequestReadTimeout [handshake=...] [header=...] [body=...]` (server config, vhost). Unfinished stages give `408 REQUEST TIME OUT`.

Default:
```apache
RequestReadTimeout handshake=0 header=20-40,MinRate=500 body=20,MinRate=500
```

## Forms
- `stage=timeout` fixed seconds (0 = no limit)
- `stage=timeout,MinRate=rate` extends by 1 second per `rate` bytes received
- `stage=timeout-maxtimeout,MinRate=rate` capped at maxtimeout
- All three stages at 0 disables the module for a vhost.

```apache
RequestReadTimeout handshake=5 header=10 body=30
RequestReadTimeout body=10,MinRate=1000
RequestReadTimeout header=10-30,MinRate=500
```

## Notes
- With an accept filter (common on Linux and FreeBSD) handshake and header timeouts start only after the process receives the socket.
- Allow for slow CRL checks in handshake timeouts.
- security_tips lists it for DoS defence, with lower `Timeout`/`KeepAliveTimeout` and the `LimitRequest*` directives.

## Checked

2026-11-08. RequestReadTimeout syntax, default, MinRate forms, 408 response, accept-filter note and CRL note confirmed on the full mod_reqtimeout page; Timeout-related DoS advice and LimitRequest* directives confirmed on security_tips.

Method: documentation only; no commands were run.
