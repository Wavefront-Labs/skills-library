---
id: computing-software.cryptography-implementation.protocol-implementation.acme-issuance-and-renewal
name: acme-issuance-and-renewal
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [cryptography-implementation, protocol-implementation, certificate-lifecycle, acme, acme-renewal, rfc8555, certbot, lego, cert-manager, dns-01, http-01, tls-alpn-01]
level: practitioner
status: docs-checked
description: "Automate certificate issuance and renewal with ACME (RFC 8555): choosing http-01, dns-01 or tls-alpn-01, certbot setup, deploy hooks, renewal timing and staging."
sources: ["https://datatracker.ietf.org/doc/html/rfc8555", "https://letsencrypt.org/docs/challenge-types/", "https://eff-certbot.readthedocs.io/en/stable/using.html", "https://cert-manager.io/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACME issuance and renewal

ACME (RFC 8555) automates domain validation and certificate issuance (Let's
Encrypt and many other CAs). With certificate lifetimes shrinking, manual renewal
is no longer viable.

## Pick the challenge

| Challenge | Proves | Needs | Use when |
|---|---|---|---|
| http-01 | control of port 80 at the name | inbound HTTP on :80; cannot issue wildcards | single public web servers |
| dns-01 | control of DNS zone | API access to DNS (TXT records); can issue wildcards | wildcards, internal hosts, load-balanced fleets |
| tls-alpn-01 | control of port 443 (RFC 8737) | TLS server that answers the ACME ALPN; cannot issue wildcards | port 80 unavailable |

For dns-01, CNAME- or NS-delegate `_acme-challenge` to a dedicated zone (Let's
Encrypt documents this), or use a DNS API token restricted to those records, so a
leaked token cannot rewrite the zone.

## Tools

```bash
# certbot (http-01, webroot), deploy hook reloads the server
certbot certonly --webroot -w /var/www/html -d example.com -d www.example.com \
  --key-type ecdsa --deploy-hook "systemctl reload nginx"
certbot renew --dry-run          # run `certbot renew` from a scheduler
```

Other ACME clients (lego, cert-manager and so on) were not checked here; read their
own documentation.

## Operational rules

- Renew early: certbot 4.0.0 and later renews when less than 1/3 of the lifetime remains
  (1/2 for lifetimes of 10 days or less); earlier versions used a fixed 30 days.
- Test against the staging endpoint first
  (`--test-cert` / `https://acme-staging-v02.api.letsencrypt.org/directory`):
  production rate limits (see the CA's rate-limit page) can block you for days.
- Deploy hook must reload every consumer (web server, mail server, load
  balancer upload); many outages come from renewed-but-not-reloaded certs.
- Protect the ACME account key; it can revoke your certificates.
- Use CAA DNS records to restrict which CAs may issue for your domains.

## Verify

- [ ] `certbot renew --dry-run` (or equivalent) succeeds unattended.
- [ ] The served certificate's notAfter changes after a forced renewal (`--force-renewal` on staging).
- [ ] CAA record present; expiry monitoring alerts independently of the ACME client.

## Checked

2026-10-31. Confirmed: Let's Encrypt challenge-types page (http-01 on port 80 only and no wildcards, dns-01 wildcards and
CNAME/NS delegation of `_acme-challenge`, tls-alpn-01 on 443 as RFC 8737 and no wildcards); certbot user guide
(`--webroot -w`, `--key-type ecdsa`, `--deploy-hook`, `--test-cert`, `--force-renewal`, `renew --dry-run`, renewal
threshold of 1/3 lifetime from 4.0.0, previously fixed 30 days); the staging directory URL answers. Removed as unconfirmed:
the lego command, the cert-manager 2/3 renewal claim, the systemd timer schedule, named CAs other than Let's Encrypt,
Traefik/Caddy tls-alpn-01 support, named rate limits and CAA `accounturi`.
Method: documentation only; no commands were run.
