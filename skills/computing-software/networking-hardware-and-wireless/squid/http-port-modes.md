---
id: computing-software.networking-hardware-and-wireless.squid.http-port-modes
name: http-port-modes
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, http-port, intercept, tproxy, accel, ssl-bump]
level: practitioner
status: docs-checked
description: "Choose the right http_port mode (forward, intercept, tproxy, accel, ssl-bump) and its main options."
sources:
  - https://www.squid-cache.org/Doc/config/http_port/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http_port modes
Syntax: `port [mode] [options]`, `hostname:port [mode] [options]` or `1.2.3.4:port [mode] [options]`; repeat the directive for several addresses. Squid normally listens on port 3128; the suggested configuration is `http_port 3128`.

Modes:
- none: default forward proxy
- `intercept`: IP-layer NAT redirected traffic; disables authentication on the port
- `tproxy`: Linux TPROXY or BSD divert-to, spoofs client IPs; also disables authentication
- `accel`: reverse proxy; options `defaultsite=`, `no-vhost`, `vport`, `protocol=`, `ignore-cc`, `act-as-origin`
- `ssl-bump`: decrypt CONNECT traffic allowed by `ssl_bump`

Other options: `tls-cert=`, `tls-key=`, `cipher=`, `options=`, `tls-dh=`, `clientca=`, `generate-host-certificates=`, `name=`, `require-proxy-header` (PROXY protocol v1 or v2), `tcpkeepalive`.

On a dual-homed host, specify the internal address:port.

## Checked

2026-11-04. Read the http_port directive page and confirmed the intercept, tproxy, accel and ssl-bump modes, the accel options, require-proxy-header, name=, tcpkeepalive, tls-dh= and the dual-homed note. Nothing was removed.

Method: documentation only; no commands were run.
