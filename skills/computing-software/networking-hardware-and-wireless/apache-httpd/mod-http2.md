---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-http2
name: mod-http2
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, http2, mod-http2, protocols, h2, h2c, early-hints]
level: practitioner
status: docs-checked
description: "Enable HTTP/2 with the Protocols directive and tune mod_http2: h2 vs h2c, H2Direct, stream limits, push, early hints and shared-certificate vhost caveats."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_http2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_http2
Uses libnghttp2 and must be enabled with `Protocols`. `h2` is HTTP/2 over TLS; `h2c` is cleartext.
```apache
Protocols h2 http/1.1
Protocols h2 h2c http/1.1
```

## Directives
- `H2Direct`: switch on connection preamble; default on for h2c, off for h2.
- `H2Upgrade`: switch via HTTP/1.1 Upgrade; same defaults; only bodiless requests.
- `H2MaxSessionStreams` default 100; `H2WindowSize` default 65535; `H2StreamMaxMemSize` default 65536.
- `H2EarlyHints` default off; `H2EarlyHint Link "</my.css>;rel=preload;as=style"`.
- `H2Push` default on, driven by `Link: rel=preload` headers; `H2PushResource [add] path [critical]`.
- `H2ModernTLSOnly` default on: TLS 1.2+ and no RFC 7540 Appendix A ciphers.

## Workers
HTTP/2 workers use a separate pool defaulting to `ThreadsPerChild` when `H2MinWorkers`/`H2MaxWorkers` are unset.

## Shared connections
Virtual hosts sharing a certificate on one connection must have identical SSL settings (protocol, ciphers, client verification) or clients get 421 Misdirected Request.

## Proxy
`H2WebSockets` enables RFC 8441 with `ProxyPass` `upgrade=websocket`; `H2ProxyRequests` is for forward proxying.

## Checked
2026-11-04. Confirmed against the mod_http2 reference: directive defaults, H2Direct/H2Upgrade behaviour, H2EarlyHint(s), H2Push and Link rel=preload, H2ModernTLSOnly, worker defaults, 421 for mismatched shared-certificate vhosts, H2WebSockets with ProxyPass upgrade=websocket. Removed: the version tag on H2EarlyHint.
Method: documentation only; no commands were run.
