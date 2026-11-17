---
id: computing-software.systems-network-administration.coredns.coredns-forward-tls-and-doh
name: coredns-forward-tls-and-doh
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, forward, dot, doh, tls, tls-servername]
level: advanced
status: docs-checked
description: "Forward over DNS-over-TLS or DoH with tls and tls_servername, including per-endpoint server names and the man-in-the-middle warning."
sources:
  - https://coredns.io/plugins/forward/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt traffic to upstream resolvers safely.

`tls CERT KEY CA` takes 0 to 3 arguments:
- `tls`: no client auth, system CAs verify the server.
- `tls CA`: no client auth, CA file verifies the server.
- `tls CERT KEY`: client auth, system CAs verify the server.
- `tls CERT KEY CA`: client auth, CA file verifies the server.

CoreDNS sets the minimum TLS version to 1.2; the maximum, cipher suites and key exchange use Go crypto/tls defaults.

`tls_servername NAME` sets the server name. Using TLS forwarding without it lets anyone man-in-the-middle the connection, so the docs strongly recommend it (9.9.9.9 needs `dns.quad9.net`).

Per-endpoint form: `tls://9.9.9.9%dns.quad9.net`. Do not combine it with `tls_servername`. For a port other than 853 append it: `tls://9.9.9.9%dns.quad9.net:10853`.

The TLS config is global for the whole forward proxy. To use different server names for different upstreams, run separate forward servers on other ports and point to them:

```
. { forward . 127.0.0.1:5301 127.0.0.1:5302 }
.:5301 { forward . tls://8.8.8.8 tls://8.8.4.4 { tls_servername dns.google } }
```

DoH uses the fixed /dns-query path (no custom paths) and `doh_method GET|POST`, default POST.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/forward/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
