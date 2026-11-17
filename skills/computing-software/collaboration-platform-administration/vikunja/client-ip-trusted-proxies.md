---
id: computing-software.collaboration-platform-administration.vikunja.client-ip-trusted-proxies
name: client-ip-trusted-proxies
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, ipextractionmethod, trustedproxies, x-forwarded-for, real-client-ip]
level: advanced
status: docs-checked
description: "Make Vikunja log and rate-limit the real client behind a reverse proxy with service.ipextractionmethod and service.trustedproxies, without allowing spoofing."
sources:
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/reverse-proxies.mdx
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default `service.ipextractionmethod` is `direct`: the TCP remote address. Behind a proxy that is the proxy, so rate limits and Fail2Ban see one client.

Methods:
- `direct`: use when Vikunja faces the internet.
- `xff`: read `X-Forwarded-For`; use behind nginx, Traefik or cloud load balancers. Preferred behind a proxy.
- `realip`: read `X-Real-IP`, honoured only when the value itself is in a trusted range (loopback, private networks or `service.trustedproxies`). It cannot report public client IPs.

```
service:
    ipextractionmethod: xff
    trustedproxies: 127.0.0.1/32,::1/128
```

Environment form: `VIKUNJA_SERVICE_IPEXTRACTIONMETHOD` and `VIKUNJA_SERVICE_TRUSTEDPROXIES`. `trustedproxies` is a comma-separated CIDR list; with `xff` the header is trusted only from those addresses.

Keep it narrow. A broad range such as `10.0.0.0/8` lets any client on that network, if it can reach Vikunja directly, choose its apparent address. List only the addresses your proxy connects from.

This feeds the `ratelimit` options and Fail2Ban.

## Checked

2026-11-04: checked against the reverse proxies page (Client IP addresses section) and config-raw.json (service.ipextractionmethod, service.trustedproxies).

Method: documentation only; no commands were run.
