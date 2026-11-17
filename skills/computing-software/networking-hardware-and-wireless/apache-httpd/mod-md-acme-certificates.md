---
id: computing-software.networking-hardware-and-wireless.apache-httpd.mod-md-acme-certificates
name: mod-md-acme-certificates
category: computing-software
field: networking-hardware-and-wireless
product: apache-httpd
tags: [networking-hardware-and-wireless, apache-httpd, mod-md, acme, letsencrypt, mdomain, certificate-renewal, tls-alpn]
level: advanced
status: docs-checked
description: "Obtain and renew ACME certificates automatically with mod_md: MDomain, agreement and contact, challenge types, renewal window, HTTPS redirect and monitoring."
sources:
  - https://httpd.apache.org/docs/2.4/mod/mod_md.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mod_md automatic certificates
Experimental, since 2.4.30, needs `mod_watchdog`, defaults to Let's Encrypt.

```apache
MDContactEmail admin@example.org
MDCertificateAgreement accepted
MDomain example.org www.example.org

<VirtualHost *:443>
    ServerName example.org
    SSLEngine on
</VirtualHost>
```
Until a certificate exists, requests get 503. `MDomain` mode `auto` adds ServerName/ServerAlias values; `manual` needs the exact list. You must accept the CA terms yourself.

## Directives
- `MDCertificateAuthority` (`letsencrypt`, `buypass`, or URL); `MDPrivateKeys` default `RSA 2048`.
- `MDRenewWindow` default `33%`.
- `MDRequireHttps` `off`/`temporary`/`permanent` (permanent adds HSTS for half a year; hard to reverse).
- `MDStoreDir` default `md`; `MDStapling` default off.
- `MDMessageCmd` / `MDNotifyCmd` run on events.

## Challenges
`http-01` needs port 80 (see `MDPortMap`); `tls-alpn-01` needs 443 and `Protocols h2 http/1.1 acme-tls/1`; `dns-01` needs `MDChallengeDns01`. `MDCAChallenges` defaults to `tls-alpn-01 http-01 dns-01`. Wildcards require dns-01; the script gets `setup` and `teardown` calls.

## Monitoring
```apache
<Location "/md-status">
  SetHandler md-status
  Require host example.com
</Location>
```
Protect it with authorisation; it exposes domain information.

## Checked
2026-11-04. Confirmed against the mod_md reference: experimental status, 2.4.30, mod_watchdog, 503 until a certificate exists, directive defaults, challenge types and prerequisites, wildcard dns-01 with setup/teardown, md-status handler, MDRequireHttps permanent HSTS. Nothing removed.
Method: documentation only; no commands were run.
