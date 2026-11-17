---
id: computing-software.networking-hardware-and-wireless.unbound.dns-over-https-server
name: dns-over-https-server
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, dns-over-https, doh, http2, nghttp2, https-port]
level: advanced
status: docs-checked
description: "Enable downstream DNS-over-HTTPS in Unbound: build with libnghttp2, set the endpoint and buffers, test with dohclient and read status codes."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/topics/privacy/dns-over-https.html
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns over https server
DoH requires TLS and works only over HTTP/2 negotiated by ALPN, using nghttp2. Build with `./configure --with-libnghttp2`. Only `application/dns-message` is supported.

```
server:
    interface: 127.0.0.1@443
    tls-service-key: "key.pem"
    tls-service-pem: "cert.pem"
```

Options: `https-port` (443), `http-endpoint` (`/dns-query`), `http-max-streams` (100), `http-query-buffer-size` and `http-response-buffer-size` (4m each), `http-nodelay` (yes), `http-notls-downstream` (no; for local backends). `harden-large-queries` limits payload to 512 bytes; otherwise `msg-buffer-size` applies.

Status codes: 200 processed (including SERVFAIL), 400 no valid query, 404 path differs from `http-endpoint`, 413 POST too large, 414 GET too large, 415 unsupported content-type, 501 method not GET or POST.

Test: `make dohclient`, then `./dohclient -s 127.0.0.1 nlnetlabs.nl AAAA IN`. Metrics: `num.query.https`, `mem.http.query_buffer`, `mem.http.response_buffer`.

DoH cannot be combined with PROXYv2 or DNSCrypt.

## Checked
2026-11-04. Confirmed against the DNS-over-HTTPS topic page and the unbound.conf manual (https-port 443, http-endpoint, http-max-streams 100, buffer and nodelay options, status codes, metrics). Removed the 1.12.0 version statement, which the pages do not state.
Method: documentation only; no commands were run.
