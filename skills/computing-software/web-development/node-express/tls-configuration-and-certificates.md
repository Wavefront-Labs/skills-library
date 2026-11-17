---
id: computing-software.web-development.node-express.tls-configuration-and-certificates
name: tls-configuration-and-certificates
category: computing-software
field: web-development
product: node-express
tags: [tls-configuration, mozilla-ssl-config, certificates, lets-encrypt, ssl-labs, https]
level: practitioner
status: docs-checked
description: "Configuring TLS for web servers: Mozilla intermediate/modern profiles, nginx settings, automated ACME certificate renewal, shrinking certificate lifetimes, CAA and testing."
sources:
  - https://ssl-config.mozilla.org/
  - https://github.com/mozilla/ssl-config-generator/blob/master/docs/guidelines/latest.json
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html
  - https://github.com/cabforum/servercert/blob/main/docs/BR.md
  - https://letsencrypt.org/docs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS configuration and certificates

## 1. Use a generated profile
Mozilla SSL Configuration Generator (ssl-config.mozilla.org) for your server and version:
- **Intermediate** (default choice): TLS 1.2 + 1.3, ECDHE with AES-GCM/ChaCha20 only.
- **Modern**: TLS 1.3 only, when you control all clients.
```nginx
server {
  listen 443 ssl; listen [::]:443 ssl; http2 on;
  ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;   # full chain, not leaf only
  ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
  ssl_protocols TLSv1.2 TLSv1.3;
  ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
  ssl_prefer_server_ciphers off;
  ssl_session_cache shared:SSL:10m; ssl_session_timeout 1d; ssl_session_tickets off;
  add_header Strict-Transport-Security "max-age=63072000" always;
}
server { listen 80; return 301 https://$host$request_uri; }
```
Node apps usually sit behind a proxy/load balancer that terminates TLS; if Node terminates, set `minVersion: "TLSv1.2"`.

## 2. Certificates
- Automate with ACME: certbot (`certbot --nginx -d example.com -d www.example.com`), acme.sh, Caddy (automatic), cert-manager on Kubernetes, or the cloud LB's managed certs.
- Lifetimes are shrinking (the CA/Browser Forum Baseline Requirements set a 47 day maximum from 2029-03-15); plan for automated renewal. Alert on expiry < 14 days.
- Let's Encrypt turned off its OCSP service on 2025-08-06 and publishes revocation through CRLs only; do not depend on OCSP stapling for its certificates.
- Add a CAA DNS record restricting which CAs may issue (`example.com. CAA 0 issue "letsencrypt.org"`).

## 3. Test
- SSL Labs (ssllabs.com/ssltest) target A/A+; `testssl.sh example.com` for CI/internal hosts.
- `openssl s_client -connect example.com:443 -servername example.com -showcerts` to inspect the chain.

## Gotchas
- Missing intermediate certificate: can appear to work in some browsers yet fail in other clients; always serve the full chain.
- Renewal hooks must reload the server (`--deploy-hook "systemctl reload nginx"`).

## Verify
- [ ] SSL Labs grade A or better; certificate expiry monitored; HTTP redirects to HTTPS.

## Checked

2026-10-25 against Mozilla server-side TLS guidelines 6.0, the nginx module docs, the CA/Browser Forum Baseline Requirements and Let's Encrypt documentation. Confirmed: Mozilla guidelines 6.0: intermediate is TLS 1.2 and 1.3 with the six ECDHE GCM and ChaCha20 ciphers, modern is TLS 1.3 only, HSTS min age 63072000, server preference off; nginx directives ssl_protocols, ssl_ciphers, ssl_prefer_server_ciphers, ssl_session_cache, ssl_session_timeout, ssl_session_tickets exist and the http2 directive appeared in nginx 1.25.1; Baseline Requirements: maximum subscriber certificate validity of 47 days from 2029-03-15; Let's Encrypt turned off its OCSP service on 2025-08-06 and publishes revocation through CRLs only; Let's Encrypt CAA syntax and certbot --deploy-hook.

Method: documentation only; no commands were run.
