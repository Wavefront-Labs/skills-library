---
id: computing-software.networking-hardware-and-wireless.squid.icap-service
name: icap-service
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, icap, icap-service, content-adaptation, reqmod, respmod]
level: advanced
status: docs-checked
description: "Define an ICAP adaptation service with icap_service: vectoring points, URI schemes and bypass and routing options."
sources:
  - https://www.squid-cache.org/Doc/config/icap_service/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# icap_service
Needs `--enable-icap-client`. Syntax: `icap_service id vectoring_point uri [option ...]`.

- id: unique service name
- vectoring point: `reqmod_precache`, `reqmod_postcache`, `respmod_precache`, `respmod_postcache` (postcache not yet supported)
- uri: `icap://` (port 1344, plain) or `icaps://` (TLS, typically port 11344)

Options: `bypass=on|off|1|0` (off by default, so failures return an error page), `routing=on|off|1|0` (honour X-Next-Services), `ipv6`, `on-overload`, `max-conn`, `connection-encryption`, `tls-*` for icaps.

Activate with `adaptation_access`; group with `adaptation_service_chain` and `adaptation_service_set`.
```
icap_service svcBlocker reqmod_precache icap://icap1.mydomain.net:1344/reqmod bypass=0
icap_service svcLogger reqmod_precache icaps://icap2.mydomain.net:11344/reqmod routing=on
```

## Checked

2026-11-04. Read the icap_service directive page and confirmed the syntax, build option, vectoring points, URI schemes and default ports, the bypass, routing, ipv6, on-overload, max-conn and connection-encryption options, the tls-* options and both examples. Nothing was removed.

Method: documentation only; no commands were run.
