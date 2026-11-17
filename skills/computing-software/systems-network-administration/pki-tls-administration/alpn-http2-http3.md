---
id: computing-software.systems-network-administration.pki-tls-administration.alpn-http2-http3
name: alpn-http2-http3
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [alpn-http2-http3, alpn, http2, http3, quic, nginx, pki-tls-administration]
level: practitioner
status: docs-checked
description: "How ALPN (RFC 7301) negotiates the application protocol in the TLS handshake and how nginx advertises HTTP/3 over QUIC."
sources:
  - https://www.rfc-editor.org/rfc/rfc7301
  - https://nginx.org/en/docs/http/ngx_http_v3_module.html
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALPN, HTTP/2 and HTTP/3
Goal: clients pick the best application protocol during the TLS handshake.
- ALPN (RFC 7301) is TLS extension type 16. The client lists protocol names in the ClientHello in descending order of preference; the server answers with exactly one name in the ServerHello. No extra round trip is added, and the server may associate a different certificate with each application protocol.
- Names are IANA-registered, non-empty byte strings. The server ignores names it does not recognise and should pick the most preferred one it supports that the client advertised. If it supports none, it must send a fatal `no_application_protocol` alert (code 120).
- ALPN sets properties of the connection, not the session: on resumption or ticket use, earlier ALPN contents are irrelevant and only the new handshake's values count.
- nginx HTTP/3 (module `ngx_http_v3_module`, since 1.25.0, still marked experimental) needs `--with-http_v3_module` and OpenSSL 1.1.1 or higher (0-RTT needs 3.5.1 or higher, or BoringSSL, LibreSSL or QuicTLS):
```
listen 8443 quic reuseport;
listen 8443 ssl;
add_header Alt-Svc 'h3=":8443"; ma=86400';
```
- The module page recommends the same port for HTTP/3 and HTTPS for better compatibility; `Alt-Svc` is what advertises HTTP/3 availability. `$http3` holds `h3` for HTTP/3 connections and `$ssl_alpn_protocol` (ssl module, 1.21.4) gives the protocol selected by ALPN.
Gotcha: the HTTP/3 module is experimental; test failure fallback to TCP before relying on it.
Verify:
- [ ] `$ssl_alpn_protocol` or an `openssl s_client -alpn` test shows the expected protocol.
- [ ] A client that cannot use HTTP/3 still connects over the TCP listener.

## Checked
Confirmed 2026-11-08 against RFC 7301 sections 1 and 3 and the ngx_http_v3_module page, plus `$ssl_alpn_protocol` on the ngx_http_ssl_module page. Removed (not on the cited pages): `http2 on` syntax and version, RFC 9113 cipher rule, HAProxy and Caddy snippets, curl `--http3` test, firewall and corporate-blocking advice, and the specific ALPN names beyond what the RFC states.
Method: docs-only read of cited pages, 2026-11-08
