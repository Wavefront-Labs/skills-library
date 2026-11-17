---
id: computing-software.cybersecurity-defensive.network-defence.dns-resolver-hardening
name: dns-resolver-hardening
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [dns-resolver-hardening, recursive-resolver, open-resolver, unbound, bind, response-rate-limiting, qname-minimisation]
level: practitioner
status: docs-checked
description: "Harden recursive DNS resolvers: restrict recursion to internal clients, DNSSEC validation, QNAME minimisation, rate limiting, cache poisoning defences and query logging."
sources: ["https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html", "https://bind9.readthedocs.io/en/latest/reference.html", "https://datatracker.ietf.org/doc/html/rfc9156"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DNS resolver hardening

## Unbound example
```
server:
  interface: 10.0.0.53
  access-control: 0.0.0.0/0 refuse
  access-control: 10.0.0.0/8 allow
  access-control: 192.168.0.0/16 allow
  hide-identity: yes
  hide-version: yes
  qname-minimisation: yes          # RFC 9156 privacy
  harden-glue: yes
  harden-dnssec-stripped: yes
  harden-below-nxdomain: yes
  harden-referral-path: no
  use-caps-for-id: no              # 0x20 randomisation; yes adds anti-spoofing but breaks some auth servers
  auto-trust-anchor-file: "root.key"   # DNSSEC validation
  val-clean-additional: yes
  ratelimit: 1000                  # per-zone query rate to upstreams
  ip-ratelimit: 200
  unwanted-reply-threshold: 10000000
  aggressive-nsec: yes
  log-queries: no                  # use dnstap for structured logging instead
```
## BIND equivalents
`allow-recursion { internal; };`, `allow-query-cache { internal; };`, `dnssec-validation auto;`,
`qname-minimization relaxed;`, `version "none";`, `minimal-responses yes;`.

## Controls
- **No open resolver:** recursion only for internal ranges; test from outside (`dig @<public-ip> example.com` must be refused).
- Separate authoritative and recursive roles/servers.
- Source port randomisation (default in modern resolvers) plus DNSSEC validation against cache poisoning.
- Forwarding to a protective DNS service (RPZ/threat feeds) - or RPZ locally.
- Query logging via dnstap or resolver logs into the SIEM (see dns-query-logging).
- Clients forced to internal resolvers (block outbound 53/853 elsewhere).
- Patch: resolvers have recurring CVEs; track vendor advisories.

## Verify
- [ ] External recursion test refused.
- [ ] A query for a deliberately mis-signed test zone returns SERVFAIL (validation working).
- [ ] `dig version.bind chaos txt` reveals nothing.

## Checked
2026-10-28. Confirmed against official pages: Unbound options (hide-identity, hide-version, qname-minimisation, harden-*, use-caps-for-id, auto-trust-anchor-file, val-clean-additional, ratelimit, ip-ratelimit, unwanted-reply-threshold, aggressive-nsec, log-queries), BIND options (allow-recursion, allow-query-cache, dnssec-validation, qname-minimization, minimal-responses), RFC 9156 QNAME minimisation.
Removed or rewritten: the KeyTrap mention, the dnssec-failed.org test and the blocked CISA source.
Method: documentation only; no commands were run.
