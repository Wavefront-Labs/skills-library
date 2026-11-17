---
id: computing-software.networking-hardware-and-wireless.unbound.dns-rebinding-private-address
name: dns-rebinding-private-address
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, private-address, private-domain, dns-rebinding, do-not-query-localhost]
level: practitioner
status: docs-checked
description: "Block DNS rebinding in Unbound by stripping private addresses from answers with private-address, and exempt internal domains with private-domain."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dns rebinding and private address
- `private-address: <netblock>` strips matching addresses from answers to block DNS rebinding. Default none; repeat for each range. It removes matching A, AAAA, SVCB and HTTPS records (the ipv4hint and ipv6hint parameters are checked), and the DNSSEC validator may mark such answers bogus.
- `private-domain: <domain>` lets a domain (and its subdomains) contain private addresses. Default none.
- `do-not-query-address` lists addresses Unbound must not query; `do-not-query-localhost` (default yes) adds localhost to it.
- `local-data` in your own zones is unaffected by these filters.

Typical pairing: list your internal ranges under `private-address`, then list internal zones that legitimately resolve to them under `private-domain`.

Related: `response-ip` can also rewrite or drop answers by address with the respip module.

## Checked

2026-11-08. Read private-address, private-domain, do-not-query-address and do-not-query-localhost in the unbound.conf manual. Added that SVCB and HTTPS records are filtered too and that the validator may mark such answers bogus.

Method: documentation only; no commands were run.
