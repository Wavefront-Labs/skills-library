---
id: computing-software.systems-network-administration.pki-tls-administration.nginx-sni-multiple-certs
name: nginx-sni-multiple-certs
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [nginx-sni-multiple-certs, pki-nginx, nginx, sni, default-server, ssl-reject-handshake, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Host many TLS names on one nginx IP using SNI, set a safe default server with ssl_reject_handshake and use variables for cert selection."
sources:
  - https://nginx.org/en/docs/http/configuring_https_servers.html#sni
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nginx SNI and multiple certificates
Goal: each hostname gets its own certificate, unknown names get none.
```
server { listen 443 ssl default_server; ssl_reject_handshake on; }       # nginx 1.19.4+
server { listen 443 ssl; server_name a.example.com; ssl_certificate /etc/ssl/a.pem; ssl_certificate_key /etc/ssl/a.key; }
server { listen 443 ssl; server_name b.example.com; ssl_certificate /etc/ssl/b.pem; ssl_certificate_key /etc/ssl/b.key; }
```
- Without SNI, nginx can only offer the default server's certificate: the TLS connection is set up before the HTTP request, so the requested name is unknown. SNI (RFC 6066) lets the client pass the name in the handshake; it is mandatory to implement in TLS 1.3 but some old or special clients do not use it.
- Alternatives to SNI: one IP address per HTTPS server (the oldest, most robust method), or one certificate with several names or a wildcard (a wildcard matches one level only; the SubjectAltName field length is limited). A multi-name certificate and key are best placed at `http` level so all servers share one memory copy.
- A default server with `ssl_reject_handshake on` rejects handshakes for other names, and also stops a client without SNI from reaching servers that verify client certificates against a different CA via the default server's configuration.
- Dynamic selection: `ssl_certificate $ssl_server_name.crt;` (1.15.9, OpenSSL 1.0.2+) loads a certificate on every handshake, which may hurt performance. `$ssl_server_name` is chosen by the client, so filter it through a `map` with a `default`. `ssl_certificate_cache max=N [inactive=time] [valid=time]` (1.27.4) caches certificates loaded via variables; defaults are inactive 10 seconds and valid 60 seconds.
- nginx must be built against, and dynamically linked to, an OpenSSL with SNI support; `nginx -V` prints "TLS SNI support enabled".
- Per the ssl module page, virtual servers with different certificates should listen on different IP addresses for maximum interoperability with clients that do not use SNI.
Verify:
- [ ] Each hostname returns its own certificate subject (test with `openssl s_client` and its server-name option).
- [ ] An unknown name gets a handshake failure.

## Checked
Confirmed 2026-11-08 against "Configuring HTTPS servers" (SNI, name-based servers, client certificates sections) and ngx_http_ssl_module (ssl_reject_handshake 1.19.4, variables in ssl_certificate 1.15.9, ssl_certificate_cache 1.27.4 and defaults). Removed: Python 2.7 and Android 2.x client claim (not on the pages).
Method: docs-only read of cited pages, 2026-11-08
