---
id: computing-software.systems-network-administration.headscale.tls-reload-renewal
name: tls-reload-renewal
category: computing-software
field: systems-network-administration
product: headscale
tags: [headscale, sighup, reload, renewal, certmagic]
level: practitioner
status: docs-checked
description: "Reload Headscale certificates and policy without restart via SIGHUP, how CertMagic renews, and why systemctl reload can report success on failure."
sources:
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/tls.md
  - https://raw.githubusercontent.com/juanfont/headscale/main/docs/ref/policy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reload and renewal

```
sudo systemctl reload headscale
sudo kill -HUP $(pidof headscale)
```

Both send SIGHUP, which reloads the certificate, key and policy file.

- New connections get the new certificate; open connections keep the old one.
- On failure to load, or an expired or not-yet-valid certificate, Headscale logs an error and keeps the previous certificate.
- Success is logged as `TLS certificate reloaded`.

## Gotcha

`systemctl reload` reports success even when the reload fails. Always check the log or the served certificate.

## ACME renewal (CertMagic)

- Let's Encrypt certificates are valid for 3 months.
- Renewal starts when a third of the validity remains.
- Renewal checks run every 10 minutes.

## Check what clients see

```
openssl s_client -servername [hostname] -connect [hostname]:443 | openssl x509 -noout -dates
```

## Policy

The same SIGHUP applies a changed policy file (policy-basics).

## Checked

2026-11-04. Confirmed against the Headscale TLS and policy pages: SIGHUP via systemctl reload or kill -HUP, certificate and policy reload, keep-previous-certificate on failure, the success log line, the systemctl caveat, and the CertMagic renewal figures (3 months, a third remaining, 10-minute checks).
Method: documentation only; no commands were run.
