---
id: computing-software.networking-hardware-and-wireless.caddy.wildcard-certificates
name: wildcard-certificates
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [wildcard-certificates, dns-challenge, subdomains, force-automate, privacy, caddyfile, automatic-https]
level: advanced
status: docs-checked
description: "Caddy wildcard certificates: qualifying names, literal site names, the 2.10 subdomain reuse change, DNS challenge and privacy limits."
sources:
  - https://caddyserver.com/docs/automatic-https
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use one certificate for many subdomains safely.

Only the left-most label may be a wildcard: `*.example.com` qualifies, while `sub.*.example.com`, `foo*.example.com`, `*bar.example.com` and `*.*.example.com` do not. In a Caddyfile, site names are taken literally for certificate subjects: a site `sub.example.com` produces a certificate for that name, and `*.example.com` produces a wildcard. JSON config gives finer control over subjects versus host matchers.

Since Caddy 2.10, when a wildcard certificate is automated, Caddy uses it for individual subdomains in the config and does not obtain per-subdomain certificates unless explicitly configured, for example with `force_automate`.

Let's Encrypt requires the DNS challenge for wildcard certificates, so configure a DNS provider module.

When to use: the page says wildcards represent a wide degree of authority. Use them when you have so many subdomains that individual certificates would strain the PKI or hit CA rate limits, or when the privacy tradeoff (not publishing every subdomain in certificate transparency logs) is worth the exposure if the key is compromised. They do not hide subdomain names: those still appear in TLS ClientHello packets unless Encrypted ClientHello is enabled.

## Checked

2026-11-08. Read the Automatic HTTPS page in full (Wildcard certificates, ECH and Hostname requirements sections). Confirmed: only the left-most label may be a wildcard with the four non-qualifying examples, literal site names in the Caddyfile, JSON giving finer control, the Caddy 2.10 behaviour with `force_automate`, the wide-authority and rate-limit rationale, subdomains still visible in ClientHello without ECH, and the Let's Encrypt DNS challenge requirement. Removed the unread claim about `host` matchers and the Caddyfile patterns page.

Method: documentation only; no commands were run.

