---
id: computing-software.networking-hardware-and-wireless.kea.control-channel-http-https-and-authentication
name: control-channel-http-https-and-authentication
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, control-channel, http, https, basic-auth, curl]
level: advanced
status: docs-checked
description: "Expose the Kea control channel over HTTP or HTTPS with socket-address, socket-port, TLS settings and basic authentication, and call it with curl."
sources:
  - https://kea.readthedocs.io/en/latest/arm/dhcp4-srv.html
  - https://kea.readthedocs.io/en/latest/arm/ctrl-channel.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea HTTP/HTTPS control socket
`socket-type` is "http" or "https" (TLS required for https). `socket-address` defaults to 127.0.0.1 and `socket-port` to 8000. `http-headers` (since 2.7.5) adds extra response headers. Multiple HTTP/HTTPS connections are supported since 2.7.6; IPv4 and IPv6 both work.

TLS: `trust-anchor`, `cert-file`, `key-file`, `cert-required`. If they are not specified, plain HTTP is used.

Basic authentication goes in an `authentication` block with mandatory `type` of "basic" (the only type). `realm` defaults to kea-dhcpv4-server. A non-empty `clients` list turns authentication on; each client needs a non-empty user id with no colon, and an optional password (empty if absent). To keep secrets out of the config, use `directory` plus `user-file` and `password-file`. Credentials are UTF-8, but Kea JSON supports only the Latin-1 subset.

Basic auth protects against local users; for remote attackers the docs say HTTPS and a reverse proxy are stronger.

Call it with curl:

```
curl -X POST -H "Content-Type: application/json" \
  -d '{ "command": "config-get" }' http://kea.example.org:8000/
```

## Checked
2026-11-04. Confirmed against the Kea Administrator Reference Manual (DHCPv4 chapter HTTP/HTTPS Control Socket and Management API chapter (curl example)). Removed: nothing.
Method: documentation only; no commands were run.
