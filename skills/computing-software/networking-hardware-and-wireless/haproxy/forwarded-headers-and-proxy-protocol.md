---
id: computing-software.networking-hardware-and-wireless.haproxy.forwarded-headers-and-proxy-protocol
name: forwarded-headers-and-proxy-protocol
category: computing-software
field: networking-hardware-and-wireless
product: haproxy
tags: [networking-hardware-and-wireless, haproxy, forwardfor, x-forwarded-for, proxy-protocol, send-proxy-v2, accept-proxy, set-src]
level: practitioner
status: docs-checked
description: "Pass the real client IP to backends in HAProxy with option forwardfor, option forwarded and PROXY protocol send-proxy-v2/accept-proxy."
sources:
  - https://docs.haproxy.org/3.0/configuration.html
  - https://www.haproxy.org/download/3.0/doc/proxy-protocol.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forwarded headers and proxy protocol
For HTTP mode add `option forwardfor` (header `X-Forwarded-For`; `header <name>` renames it, `except <network>` skips matching sources, `if-none` adds it only when absent) or `option forwarded` for the standard `Forwarded` header (default `proto for`).

```
defaults
    option forwardfor except 127.0.0.0/8
frontend fe_edge
    bind :443 ssl crt /etc/haproxy/certs/ accept-proxy   # only when an LB in front sends PROXY
    http-request set-header X-Forwarded-Proto https if { ssl_fc }
backend be_tcp
    server db 10.0.0.30:5432 check send-proxy-v2
```
HAProxy always appends `X-Forwarded-For` at the end of the header list, so the server must use only the last occurrence (a client may already have sent one). `if-none` is only safe in a perfectly trusted environment.

For TCP services or non-HTTP, use the PROXY protocol: `send-proxy-v2` on a `server` line tells the backend the client's layer 3/4 addresses (and ALPN when negotiated). The server must understand that version of the protocol. v2 is the binary header format (v1 is human-readable). `send-proxy-v2-ssl` adds the SSL information extension, `send-proxy-v2-ssl-cn` also the client certificate CN, and `proxy-v2-options` selects more fields (`ssl-cipher`, `authority`, `unique-id` and others).

Behind a trusted proxy or CDN, `http-request set-src hdr(x-forwarded-for)` (or another header your proxy sets) makes ACLs and stick tables use the forwarded address; do it only for requests from the proxy's source range, otherwise clients can spoof their IP.

Gotcha: `accept-proxy` on a public port lets anyone forge client IPs; use `tcp-request connection expect-proxy layer4 if { src 10.0.0.0/8 }` to accept the header only from chosen sources (the docs describe it as the same as `accept-proxy` but limited by an ACL).

Verify: the backend logs show the client IP; a client-supplied `X-Forwarded-For: 1.2.3.4` arrives followed by the real address as the last value.

## Checked
2026-11-03. Confirmed against configuration.html (`option forwardfor`, `option forwarded`, bind `accept-proxy`, server `send-proxy-v2`, `send-proxy-v2-ssl`, `send-proxy-v2-ssl-cn`, `proxy-v2-options`, `tcp-request connection expect-proxy layer4`, `http-request set-src`) and proxy-protocol.txt (v1 human-readable, v2 binary). Removed: the hand-built `Forwarded` header via `set-header`, the NGINX/Postgres pooler examples, the `CF-Connecting-IP` header (a CDN-specific claim), "connections fail with garbage errors", and "v2 carries TLS info" in that form.
Method: documentation only; no commands were run.
