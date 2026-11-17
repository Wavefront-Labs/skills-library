---
id: computing-software.cryptography-implementation.protocol-implementation.nginx-tls-configuration
name: nginx-tls-configuration
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, nginx-tls, nginx, tls-configuration, tls-server-config, hsts, mtls, ssl-ecdh-curve, session-tickets]
level: practitioner
status: verified
description: "Configure nginx TLS: full chain, protocols and ciphers, ECDH curves, session tickets, HSTS, mTLS client verification, ssl_conf_command and safe reloads."
sources: ["https://nginx.org/en/docs/http/ngx_http_ssl_module.html", "https://nginx.org/en/docs/http/configuring_https_servers.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# nginx TLS configuration

## Baseline (Mozilla "intermediate" style)
```nginx
server {
    listen 443 ssl;
    http2 on;
    server_name example.com;

    ssl_certificate     /etc/ssl/example/fullchain.pem;   # leaf + intermediates, no root
    ssl_certificate_key /etc/ssl/example/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    ssl_ecdh_curve prime256v1:secp384r1;     # default is auto; hybrid PQ groups depend on your OpenSSL build

    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;          # or rotate ticket keys (ssl_session_ticket_key files) across the fleet

    add_header Strict-Transport-Security "max-age=63072000" always;
}
server { listen 80; server_name example.com; return 301 https://$host$request_uri; }
```
- `ssl_conf_command` (nginx 1.19.4+) passes raw OpenSSL settings, e.g. `ssl_conf_command Ciphersuites TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256;`.
- Dual certificates: repeat `ssl_certificate`/`ssl_certificate_key` pairs (one ECDSA, one RSA).
- OCSP stapling uses `ssl_stapling on; ssl_stapling_verify on;` plus a `resolver`; only useful if your CA still publishes OCSP.

## Client certificates (mTLS)
```nginx
ssl_client_certificate /etc/ssl/clients/ca.pem;   # trusted CAs, also sent as acceptable CA names
ssl_verify_client on;                              # or optional + check $ssl_client_verify per location
ssl_verify_depth 2;
proxy_set_header X-Client-Verify $ssl_client_verify;
proxy_set_header X-Client-DN $ssl_client_s_dn;
```
Strip any incoming `X-Client-*` headers so clients cannot spoof them.

## Safe changes
```
nginx -t && systemctl reload nginx
openssl s_client -connect example.com:443 -servername example.com -brief </dev/null
```

## Gotchas
- `ssl_certificate` with only the leaf leaves clients without the intermediates; serve the full chain.
- Since 1.25.1 the `ssl` directive is removed; use the `ssl` parameter of `listen`.
- Defaults are `ssl_protocols TLSv1.2 TLSv1.3` and `ssl_ciphers HIGH:!aNULL:!MD5`.
- Private key must be readable by nginx's master process; keep access restricted.

## Verify
- [ ] testssl.sh/SSLyze show only TLS 1.2/1.3 and the intended suites.
- [ ] Full chain served; HSTS header present.

## Checked
2026-11-01. Confirmed against nginx ngx_http_ssl_module and configuring_https_servers pages: ssl_conf_command (1.19.4), ssl_ecdh_curve default auto, ssl_prefer_server_ciphers, ssl_verify_depth, default protocols and ciphers, ssl directive removed in 1.25.1, master-process key access. Removed: PQ curve example, Let's Encrypt OCSP date, Android/Java claim, ssl_protocols-ignored claim, 0600 mode.
Run 2026-11-01 on nginx 1.30.6 (Windows, OpenSSL 3.2 s_client, self-signed certificates, 127.0.0.1 only; ports changed): the baseline block with `http2 on`, the cipher list, `ssl_ecdh_curve prime256v1:secp384r1`, `ssl_session_cache`, `ssl_session_tickets off`, HSTS and `ssl_conf_command Ciphersuites ...` passes `nginx -t`; TLS 1.2 negotiated ECDHE-RSA-AES256-GCM-SHA384 and TLS 1.3 TLS_AES_256_GCM_SHA384; a client offering only TLS_CHACHA20_POLY1305_SHA256 was rejected (so `ssl_conf_command Ciphersuites` is enforced); no session ticket was issued with tickets off; the `Strict-Transport-Security` header is sent on a 404 because of `always`; mTLS with `ssl_verify_client on` returned 400 "No required SSL certificate was sent" without a certificate and `$ssl_client_verify`=SUCCESS with `$ssl_client_s_dn`=CN=client1 with one; `nginx -t` then `-s reload` succeeded; the old `ssl on;` directive fails with `unknown directive "ssl"`. Not run: dual certificates, `ssl_session_ticket_key` rotation, OCSP stapling (no issuer for a self-signed certificate), testssl.sh/SSLyze and `systemctl reload`.
