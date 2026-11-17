---
id: computing-software.systems-network-administration.pki-tls-administration.acme-challenge-types
name: acme-challenge-types
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [acme-challenge-types, pki-acme-protocol, acme, http-01, dns-01, tls-alpn-01, pki-tls-administration]
level: practitioner
status: docs-checked
description: "Choose http-01, dns-01 or tls-alpn-01 for each environment and know the requirements, ports and wildcard limits."
sources:
  - https://www.rfc-editor.org/rfc/rfc8555
  - https://letsencrypt.org/docs/challenge-types/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME challenge types
Goal: pick the validation method that fits the host.
| Challenge | Proof | Notes |
|---|---|---|
| http-01 | file at `/.well-known/acme-challenge/<token>` on port 80 | simple, no wildcards, needs inbound 80 |
| dns-01 | TXT `_acme-challenge.<name>` | wildcards, works behind firewalls, needs DNS API |
| tls-alpn-01 | TLS handshake with a custom ALPN protocol on port 443 (RFC 8737) | no port 80, no wildcards, needs an ALPN-aware server |
- Let's Encrypt http-01 follows up to 10 redirects, only to `http:` or `https:` URLs on ports 80 or 443, and does not validate certificates on HTTPS redirects.
- dns-01: a CNAME or NS record can delegate `_acme-challenge` to another zone, for example a validation-only zone so the DNS credential has less reach, or a faster-updating server.
- Several TXT records may exist at once (wildcard plus non-wildcard); clean up old ones because an oversized response is rejected.
- Some DNS APIs give no propagation time information, so poll before asking the CA to validate.
Gotcha: http-01 can only use port 80 (the ACME standard forbids other ports) and fails if an ISP blocks it; use dns-01 or tls-alpn-01 then.
Verify:
- [ ] `curl -I http://host/.well-known/acme-challenge/test` reaches origin, not a block page.
- [ ] `dig +short TXT _acme-challenge.host @ns` shows the token during validation.

## Checked
2026-11-03. Confirmed on the Let's Encrypt Challenge Types page: http-01 on port 80 only, no wildcards, redirect rules (10 deep, ports 80 or 443); dns-01 allows wildcards and CNAME or NS delegation of `_acme-challenge`, multiple TXT records, propagation caveat; TLS-ALPN-01 on port 443, RFC 8737, no wildcards. Removed: `acme-tls/1` and the self-signed wording, the 60 second TTL, the IPv6-first claim and the CDN/WAF caching gotcha (none is on the page).
Method: documentation only; no commands were run.
