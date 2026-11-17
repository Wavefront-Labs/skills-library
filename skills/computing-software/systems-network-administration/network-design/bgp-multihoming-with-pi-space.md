---
id: computing-software.systems-network-administration.network-design.bgp-multihoming-with-pi-space
name: bgp-multihoming-with-pi-space
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, bgp-multihoming, bgp, provider-independent, asn, rpki, roa, irr, dual-isp]
level: practitioner
status: docs-checked
description: "Design dual-ISP BGP multihoming with your own ASN and provider-independent prefix: RIR requests, ROAs and IRR objects, inbound and outbound traffic engineering."
sources:
  - https://www.ripe.net/manage-ips-and-asns/
  - https://www.rfc-editor.org/rfc/rfc7454
  - https://www.manrs.org/netops/guide/
  - https://www.rfc-editor.org/rfc/rfc6811
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP multihoming with PI space

Goal: stay reachable at the same addresses when either ISP fails. That needs your own
address block announced by both providers, so you need an ASN and provider-independent
(or provider-aggregatable but portable) space.

## Prerequisites
- **ASN** and **PI prefix** from your RIR (ARIN, RIPE NCC via an LIR, APNIC...). Check
  your RIR's current policy for assignment sizes and eligibility.
- **ROA** in RPKI authorising your ASN to originate the prefix; networks that validate route
  origins (RFC 6811) classify routes as Valid, Invalid or NotFound against ROAs.
- **IRR route/route6 objects**; ISPs build filters from them.
- Contracts with two ISPs offering BGP sessions, ideally diverse physical paths and different upstreams.

## Outbound (what you control fully)
- Take default only (cheap routers) or default + partial routes (customer routes of each ISP)
  for better exit choice. Full tables only if you need fine control and have the RAM.
- Local preference picks the primary exit.

## Inbound (what you can only influence)
- AS-path prepending on the backup ISP.
- ISP **communities** to lower local-pref in their network.
- Split announcements (/24s) only if you have the space; do not deaggregate needlessly.

## Must-haves (MANRS / RFC 7454)
- Outbound prefix-list allowing only your prefixes: never become transit between ISPs.
- Inbound filtering of bogons and your own prefix; maximum-prefix limits.
- Two routers, one per ISP, with iBGP between them, for router redundancy.

## Verify
- [ ] Prefix visible with your origin AS via both upstreams in public looking glasses; RPKI status Valid; failover test with one ISP shut keeps inbound and outbound working.

## Checked

- Date: 2026-10-28
- Confirmed: RIPE NCC members request IPv4 /24 allocations; RFC 6811 route-origin validation; RFC 7454 covers maximum prefixes on a peering and bogon filtering; MANRS covers IRR route objects and RPKI.
- Removed: minimum routable prefix sizes, ROA max-length detail, named IRR databases, prepend counts, bgp.tools.

Method: documentation only; no commands were run.
