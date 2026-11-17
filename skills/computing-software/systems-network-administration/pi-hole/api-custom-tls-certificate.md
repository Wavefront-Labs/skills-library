---
id: computing-software.systems-network-administration.pi-hole.api-custom-tls-certificate
name: api-custom-tls-certificate
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-tls, webserver-cert, ca-trust]
level: advanced
status: docs-checked
description: "Trust Pi-hole's self-signed CA or install your own PEM certificate for the web interface and API."
sources: ["https://docs.pi-hole.net/api/tls/", "https://docs.pi-hole.net/ftldns/configfile/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# TLS certificates for the web interface

Pi-hole creates a self-signed certificate at install, so browsers warn. There are two fixes.

**Trust the generated CA.** Import the CA file (for example `/etc/pihole/tls_ca.crt`), not the server certificate `/etc/pihole/tls.pem`, into the browser or OS as an authority trusted for websites. The certificate is only valid for the domain configured when it was created; another hostname warns again. To regenerate for a new domain, remove the old certificate and restart `pihole-FTL`. Because the CA's private key is discarded, you must import a new CA whenever the domain changes.

Android: install the CA as a user certificate from Credential storage. Recent Firefox Mobile may also need "Use third party CA certificates" enabled in Secret Settings.

**Use your own certificate.** Put the certificate and private key together in one PEM file readable by user `pihole`, then set `webserver.tls.cert` in `/etc/pihole/pihole.toml` and restart:

```bash
sudo service pihole-FTL restart
```

If you only have separate files: `cp server.crt server.pem && cat server.key >> server.pem`.

**Validity.** `webserver.tls.validity` (default 47 days, minimum 7) applies to generated certificates, which renew two days before expiry. With your own certificate set it to `0` so Pi-hole does not regenerate it.

**Checklist**

1. Pick CA import or own certificate.
2. Match the certificate domain to `webserver.domain` or the name users type.
3. Restart `pihole-FTL`.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: TLS/SSL (api/tls); FTL Configuration Reference (ftldns/configfile). Nothing needed removing.
Method: documentation only; no commands were run.
