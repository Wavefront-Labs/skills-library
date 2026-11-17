---
id: computing-software.networking-hardware-and-wireless.caddy.encrypted-clienthello-ech
name: encrypted-clienthello-ech
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [ech, encrypted-clienthello, sni, https-dns-record, grease, privacy, automatic-https]
level: sme
status: docs-checked
description: "Caddy automatic Encrypted ClientHello: hiding the SNI, HTTPS DNS record publication rules, DoH or DoT clients and GREASE."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know what Caddy automates for ECH and what you must still ensure.

Normally the ClientHello, including the SNI (the domain), is sent in plaintext. With ECH the client wraps the real ClientHello inside an outer one that establishes parameters for decrypting the inner one. The client needs ECH config (a public key and the outer "public name", among other things), which browsers fetch from HTTPS-type DNS records containing base64 ECH parameters. Caddy can generate, publish and serve ECH configs automatically. Clients must look the record up over a secure DNS protocol (DoH or DoT), otherwise plaintext DNS compromises the benefit; this may need to be enabled in the browser. Caddy then decrypts the inner ClientHello and serves the site without the domain appearing on the wire.

Publication rules: Caddy creates an HTTPS record for a domain only if a record already exists for it, so it does not break lookups of subdomains covered by a wildcard; give sites at least an A/AAAA record, and if you rely on a wildcard DNS record, the wildcard name must also appear in the Caddy config. It will not publish an HTTPS record for a domain that has a CNAME record.

GREASE: modern browsers send an `encrypted_client_hello` extension even to sites without ECH, so real ECH handshakes are indistinguishable from plaintext ones and censors cannot block them cheaply. Keep this in mind when reading packet captures: the extension does not prove ECH is in use.

## Checked

2026-11-08. Read the Automatic HTTPS page in full (Encrypted ClientHello section with its deployment considerations, enabling and verifying subsections). Confirmed: plaintext SNI problem, outer and inner ClientHello, public key and public name in the ECH config, HTTPS-type DNS records with base64 parameters, Caddy generating, publishing and serving configs, DoH or DoT need, the three publication rules (existing record, wildcard must appear in config, no CNAME), and GREASE behaviour in Firefox and Chrome.

Method: documentation only; no commands were run.
