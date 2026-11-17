---
id: computing-software.networking-hardware-and-wireless.caddy.acme-challenges-http-tls-alpn-dns
name: acme-challenges-http-tls-alpn-dns
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [acme-challenges, http-01, tls-alpn-01, dns-01, dns-challenge, cname-delegation, automatic-https]
level: practitioner
status: docs-checked
description: "Choose between ACME http-01, tls-alpn-01 and dns-01 challenges in Caddy: ports needed, default enablement, random selection and learning, and CNAME delegation."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick and troubleshoot how a certificate is validated.

HTTP challenge: after an authoritative A/AAAA lookup, the CA fetches a temporary resource over port 80. Needs port 80 externally reachable (or forwarded to Caddy's HTTP port). On by default.

TLS-ALPN challenge: the CA performs a TLS handshake on port 443 with special server name and ALPN values. Needs 443 reachable (or forwarded to the HTTPS port). On by default.

DNS challenge: the CA looks up a special `TXT` record. No open ports and no external reachability needed, but you must configure credentials for your DNS provider so Caddy can set and clear the record. Enabling it disables the other challenges by default. Provider support comes from community DNS plugin modules (documented on the Caddy wiki). Because CAs follow DNS standards, a CNAME on `_acme-challenge` can delegate validation to another zone, handy when your provider has no API; see the `tls` directive documentation for the matching option.

With several challenges enabled, Caddy picks one at random to avoid dependence on a single type, then learns which succeeds most and tries that first, falling back to the rest if needed.

Wildcard certificates require the DNS challenge at Let's Encrypt.

Use the DNS challenge for servers behind NAT or firewalls, for wildcards, and when ports 80/443 are not available.

## Checked

2026-11-03: read automatic-https against this skill. Confirmed: HTTP, TLS-ALPN and DNS challenge descriptions, ports 80/443, random choice then learned preference, CNAME delegation of _acme-challenge and wildcard needing DNS.
Removed or reworded: the named tls option for CNAME delegation (the automatic HTTPS page does not name it).
Method: documentation only; no commands were run.
