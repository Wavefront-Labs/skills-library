---
id: computing-software.systems-network-administration.pki-tls-administration.nginx-tls-server-block
name: nginx-tls-server-block
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [nginx-tls-server-block, pki-nginx, nginx, ssl-certificate, fullchain, tls-hardening, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Write a correct nginx HTTPS server block: certificate chain order, RSA plus ECDSA pair, protocols, session cache and key file permissions."
sources:
  - https://nginx.org/en/docs/http/configuring_https_servers.html
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nginx TLS server block
Goal: a correct HTTPS listener.
```
server {
  listen 443 ssl;
  server_name example.com;
  ssl_certificate     /etc/ssl/example.ecdsa.fullchain.pem;
  ssl_certificate_key /etc/ssl/example.ecdsa.key;
  ssl_certificate     /etc/ssl/example.rsa.fullchain.pem;
  ssl_certificate_key /etc/ssl/example.rsa.key;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_session_cache shared:SSL:10m;
  ssl_session_tickets off;
}
```
- Enable TLS with the `ssl` parameter of `listen` (the `ssl` directive was made obsolete in 1.15.0 and removed in 1.25.1).
- A certificate file holds the leaf first, then the intermediates. If the bundle is concatenated in the wrong order, nginx fails to start with a key values mismatch error because it tries the key against the bundle's first certificate.
- Since 1.11.0 `ssl_certificate` can be given several times to load certificates of different types (RSA and ECDSA); separate chains per certificate need OpenSSL 1.0.2 or higher. For ECDSA to work, `ssl_ecdh_curve` must include the curves the certificates use.
- The private key file should have restricted access but must be readable by nginx's master process.
- Defaults: `ssl_protocols TLSv1.2 TLSv1.3` and `ssl_ciphers HIGH:!aNULL:!MD5`, so setting them explicitly is generally not needed (defaults have changed over versions). `ssl_session_tickets` defaults to `on`; `ssl_session_cache` defaults to `none`; a 1 MB shared cache holds about 4000 sessions; `ssl_session_timeout` defaults to 5m.
- Browsers cache intermediates they have seen, so a missing chain may go unnoticed in browsers; check what the server really sends with `openssl s_client -connect HOST:443` and read the "Certificate chain" listing (without a bundle only certificate 0 appears).
Gotcha: serving the leaf alone can look fine in browsers and still fail for clients that do not cache or fetch intermediates.
Verify:
- [ ] The `s_client` chain listing shows the leaf and each intermediate.
- [ ] nginx starts with the configuration without a key mismatch error.

## Checked
Confirmed 2026-11-08 against "Configuring HTTPS servers" and ngx_http_ssl_module: listen ssl, chain order and mismatch error, multiple certificate types (1.11.0), key readability, defaults and 4000 sessions per MB. Removed (not on the cited pages): port-80 redirect, `http2 on`, HSTS header, mode 600 rule, reload command, curl and Java client claims.
Method: docs-only read of cited pages, 2026-11-08
