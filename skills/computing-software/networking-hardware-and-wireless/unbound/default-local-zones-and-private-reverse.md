---
id: computing-software.networking-hardware-and-wireless.unbound.default-local-zones-and-private-reverse
name: default-local-zones-and-private-reverse
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, default-local-zones, nodefault, unblock-lan-zones, insecure-lan-zones, reverse-dns]
level: practitioner
status: docs-checked
description: "Know the local zones Unbound creates by default (localhost, RFC 1918 reverse, special-use names) and override them with nodefault or unblock-lan-zones."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# default local zones and private reverse
Unbound ships default local zones:
- `localhost` as redirect with A 127.0.0.1 and AAAA ::1; loopback reverse zones as static.
- Static special-use names: home.arpa (RFC 8375), resolver.arpa (RFC 9462), service.arpa, onion (RFC 7686), test and invalid (RFC 6761).
- Reverse zones for RFC 1918 (10, 16-31.172, 168.192 in-addr.arpa), RFC 3330 special-use IPv4, IPv6 unspecified, ULA, link-local and the example prefix.
- AS112 zones return NXDOMAIN.

Override a default by defining your own `local-zone` for that name, or with type `nodefault` to remove its default content only.

`unblock-lan-zones: yes` (default no) stops filtering reverse lookups for private address space; only localhost reverse zones keep default content.

`insecure-lan-zones: yes` (default no) skips DNSSEC validation for the private-address reverse zones; the manual says it is usually required together with `unblock-lan-zones`.

## Checked

2026-11-08. Read the default local zone listings, unblock-lan-zones and insecure-lan-zones in the unbound.conf manual. Claims confirmed; description shortened.

Method: documentation only; no commands were run.
