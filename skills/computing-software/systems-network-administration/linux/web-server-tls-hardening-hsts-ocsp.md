---
id: computing-software.systems-network-administration.linux.web-server-tls-hardening-hsts-ocsp
name: web-server-tls-hardening-hsts-ocsp
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, nginx, apache, hsts, ocsp-stapling, ssl-protocols, tls-hardening, mozilla-ssl-config]
level: practitioner
status: docs-checked
description: "Harden TLS on nginx and Apache: protocol and cipher choices from the Mozilla guidelines, HSTS with preload caution, OCSP stapling, session settings and verifying with testssl.sh."
sources:
  - https://ssl-config.mozilla.org/
  - https://nginx.org/en/docs/http/ngx_http_ssl_module.html
  - https://httpd.apache.org/docs/2.4/mod/mod_ssl.html
  - https://testssl.sh/
  - https://hstspreload.org/
  - https://letsencrypt.org/2024/12/05/ending-ocsp/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS hardening on nginx and Apache

Start from the Mozilla SSL Configuration Generator ("intermediate" for general sites, "modern" when all clients are recent). In Mozilla's guidelines v6.0, intermediate allows TLS 1.2 and 1.3 with the six ECDHE AEAD cipher suites below, no server cipher-order preference, HSTS max-age 63072000 and OCSP stapling; modern is TLS 1.3 only.

## nginx (intermediate)
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:TLS:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/ssl/certs/chain.pem;   # issuer chain for stapling verification
resolver <dns-server-ip> valid=300s;                 # used to resolve the OCSP responder host name
add_header Strict-Transport-Security "max-age=63072000" always;
```
## Apache
```apache
SSLProtocol             -all +TLSv1.2 +TLSv1.3
SSLCipherSuite          <same list as above>
SSLHonorCipherOrder     off
SSLSessionTickets       off
SSLUseStapling          On
SSLStaplingCache        "shmcb:logs/ssl_stapling(32768)"     # global context
Header always set Strict-Transport-Security "max-age=63072000"
```
Where the system uses crypto-policies (see the system-wide-crypto-policies skill), OpenSSL-based services follow it by default unless configured explicitly; check with `update-crypto-policies --show`.

## HSTS
Start with a short `max-age`, and raise it once all subdomains are HTTPS. The preload list (hstspreload.org) requires `max-age` of at least 31536000 (1 year) plus `includeSubDomains` and `preload` on the base domain; new entries take several months to reach Chrome stable, and removal also takes a request and time, so submit only when every subdomain is ready.

## Verify externally
```bash
testssl.sh --fast https://www.example.com
openssl s_client -connect www.example.com:443 -status </dev/null | grep -A3 'OCSP Response Status'
curl -sI https://www.example.com | grep -i strict-transport
nginx -t && systemctl reload nginx ; apachectl configtest
```
OCSP: Let's Encrypt dropped OCSP URLs from certificates on 7 May 2025 and turned off its OCSP responders on 6 August 2025, so stapling does nothing for its certificates; keep it for CAs that still run OCSP. nginx needs `ssl_trusted_certificate` (issuer, root and intermediates) for `ssl_stapling_verify` to work.

## Verify
- [ ] testssl.sh shows only TLS 1.2/1.3, no weak ciphers, HSTS present; the site works in the oldest client you must support.

## Checked
Checked 2026-10-27 against Mozilla server-side TLS guidelines v6.0 (ssl-config.mozilla.org/guidelines/latest.json), the nginx ngx_http_ssl_module documentation source, the Apache mod_ssl documentation source, hstspreload.org, the Let's Encrypt OCSP end-of-life announcement and the testssl.sh script.
- Mozilla intermediate: TLS 1.2 and 1.3, the six ECDHE GCM/CHACHA20 OpenSSL cipher names used above, `server_preferred_order` false, `hsts_min_age` 63072000, OCSP staple true; modern is TLS 1.3 only.
- nginx: `ssl_stapling` and `ssl_stapling_verify` (default off, appeared in 1.3.7), `ssl_trusted_certificate` needed for verification, `ssl_session_tickets` default on, `ssl_prefer_server_ciphers` default off.
- Apache: `SSLUseStapling`, `SSLStaplingCache` (server config only, `shmcb:` type), `SSLSessionTickets` default on, `SSLHonorCipherOrder` default off, `SSLProtocol [+|-]protocol`.
- Preload list needs max-age of at least 31536000, `includeSubDomains` and `preload`; Chrome entries can take several months. Let's Encrypt: OCSP URLs dropped 7 May 2025, responders off 6 August 2025. testssl.sh has a `--fast` option.
- Removed unconfirmed claims: the "irreversible" preload wording, RHEL crypto-policy narrowing claim, and the loopback stub resolver address.
Method: documentation only; no commands were run.
