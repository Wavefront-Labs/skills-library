---
id: computing-software.systems-network-administration.dns-dhcp.doh-behind-a-reverse-proxy
name: doh-behind-a-reverse-proxy
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dns, doh-reverse-proxy, dns-over-https, nginx, encrypted-dns]
level: practitioner
status: docs-checked
description: "Serve DNS over HTTPS through a reverse proxy in front of dnsdist: cleartext backend, HTTP/2 to the backend, nginx grpc_pass, forwarded headers."
sources:
  - https://www.rfc-editor.org/rfc/rfc8484
  - https://dnsdist.org/guides/dns-over-https.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DoH behind a reverse proxy

Terminating TLS at an existing web tier lets you reuse its certificates and logging for DoH, which uses the `application/dns-message` media type under a URI template such as `https://dnsserver.example.net/dns-query{?dns}` (RFC 8484).

## Protocol facts that shape the proxy
- A DoH server must implement both GET and POST. GET carries the query base64url-encoded in the `dns` parameter; POST carries it as the body with `content-type: application/dns-message`. Requests use `accept: application/dns-message`. Example path: `/dns-query?dns=AAABAAABAAAAAAAAA3d3dwdleGFtcGxlA2NvbQAAAQAB`.
- The protocol must be used over the https scheme.
- HTTP/2 is the minimum recommended HTTP version for DoH; earlier versions can carry DoH but may perform very poorly. Keep HTTP/2 enabled at the proxy's client side.
- DoH responses carry cache freshness information; a proxy cache must not make a response fresher than the DNS TTLs allow.

## dnsdist as the backend
- To run DoH behind a reverse proxy without encrypting the proxy-to-dnsdist hop, make dnsdist listen for DoH over plain HTTP, for example on localhost port 8053: `addDOHLocal("127.0.0.1:8053")`, or in YAML a bind with `protocol: "DoH"`. The dnsdist guide also shows leaving certificates undefined with a path argument, for example `addDOHLocal("127.0.0.1:8053", nil, nil, "/", { reusePort=true })`.
- Since dnsdist 2.1.0 it uses nghttp2, which does not support HTTP/1. A reverse proxy that cannot speak HTTP/2 to the backend, such as nginx with `proxy_pass`, cannot talk to it. dnsdist recommends HTTP/2 between proxy and dnsdist.
- The nginx workaround the dnsdist guide gives is `grpc_pass` (for example `grpc_pass grpcs://dnsdist:443;`) inside `location /dns-query`, together with `proxy_set_header` lines for Host, X-Real-IP, X-Forwarded-Host, X-Forwarded-For, X-Forwarded-Proto, Range and If-Range.
- dnsdist handles DoH with two threads per bind: one for TLS and HTTP/2, one that applies rules and forwards the query to the backend over UDP (unless the backend is TCP-only or DoT).

## Client IPs
The resolver or dnsdist sees only the proxy's address unless you pass the client address along, for example in the forwarded headers above, or log at the proxy.

## Verify
- [ ] A DoH client query through the proxy returns an answer over HTTP/2, and the backend or proxy logs show the intended client address.

## Checked

Confirmed against RFC 8484 (GET/POST, media type, section 5.2 HTTP/2, https requirement, caching) and the dnsdist DNS-over-HTTPS guide (DNS over HTTP section, HTTP/1 support section, internal design). Removed: BIND, Unbound and doh-server backend settings and the BIND reference source (not read), the full nginx TLS server block and `grpc://` example with certificate paths, the `trustForwardedForHeader` setting, the claim that dnsdist accepts HTTP/1.1, and the curl and kdig test commands.

Method: docs-checked 2026-11-09 against RFC 8484 (rfc-editor.org text) and the dnsdist DoH guide (dnsdist.org HTML).
