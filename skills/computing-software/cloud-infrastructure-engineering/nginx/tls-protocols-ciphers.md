---
id: computing-software.cloud-infrastructure-engineering.nginx.tls-protocols-ciphers
name: tls-protocols-ciphers
category: computing-software
field: cloud-infrastructure-engineering
product: nginx
tags: [nginx, ssl-protocols, ssl-ciphers, tls13, ssl-certificate]
level: practitioner
status: docs-checked
description: "Configuring ssl_protocols, ssl_ciphers, ssl_prefer_server_ciphers and the certificate chain file in nginx, with the documented defaults."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/configuring_https_servers.html", "https://nginx.org/en/docs/http/server_names.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Defaults: `ssl_protocols TLSv1.2 TLSv1.3;` (TLSv1.3 is in the default since 1.23.4), `ssl_ciphers HIGH:!aNULL:!MD5;`, `ssl_prefer_server_ciphers off`, `ssl_ecdh_curve auto`.

```nginx
server {
    listen 443 ssl;
    ssl_certificate     /etc/nginx/tls/fullchain.pem;
    ssl_certificate_key /etc/nginx/tls/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

- `ssl_protocols` accepts `SSLv2 SSLv3 TLSv1 TLSv1.1 TLSv1.2 TLSv1.3`. `TLSv1.2` needs OpenSSL 1.0.1 or higher, `TLSv1.3` needs OpenSSL 1.1.1 or higher.
- `ssl_ciphers` takes the format understood by OpenSSL; list the available ciphers with `openssl ciphers`. Previous nginx versions used different default ciphers.
- `ssl_prefer_server_ciphers on` makes the server's preference win over the client's for SSLv3 and TLS.
- `ssl_conf_command` passes arbitrary OpenSSL commands, e.g. `ssl_conf_command Ciphersuites TLS_CHACHA20_POLY1305_SHA256;`; the docs warn that configuring OpenSSL directly may give unexpected behaviour.
- `ssl_certificate` should contain the primary certificate first, then the intermediates, in the same file. The HTTPS guide builds it with `cat www.example.com.crt bundle.crt > www.example.com.chained.crt`.
- `ssl_ecdh_curve` sets the curve list; for ECDSA certificates the curves used in the certificates must be included.
- Protocol choice can happen before SNI selects a server. A server-level protocol list is applied only with OpenSSL 1.1.1 or higher, BoringSSL or AWS-LC; otherwise specify `ssl_protocols` only on the default server.
- The `$ssl_protocol` and `$ssl_cipher` variables log the negotiated protocol and cipher.

## Checked
Date: 2026-11-03.
Confirmed in the ngx_http_ssl_module, configuring_https_servers and server_names pages: defaults, versions, certificate chain order and example, conf_command, ecdh curve, default-server rule, variables.
Removed as unconfirmed: the long explicit ECDHE cipher list, the claim that `ssl_ciphers` only affects TLS 1.2 and below, the browser-hardware rationale for server preference off, and the nmap/openssl verify step.
Method: documentation only; no commands were run.
