---
id: computing-software.systems-network-administration.network-design.ipv6-ula-vs-gua
name: ipv6-ula-vs-gua
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6, ula, gua, unique-local-address, global-unicast, provider-independent, address-selection]
level: practitioner
status: verified
description: "Choose between IPv6 ULA (fd00::/8) and global unicast for internal networks, generate a proper random ULA prefix, and avoid ULA address selection pitfalls."
sources:
  - https://www.rfc-editor.org/rfc/rfc4193
  - https://www.rfc-editor.org/rfc/rfc6724
  - https://datatracker.ietf.org/doc/draft-ietf-6man-rfc6724-update/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 ULA vs GUA

## The options
- **GUA** (global unicast, 2000::/3): routable, from your ISP (PA) or your own RIR
  allocation (PI). Default choice for anything that talks to the internet.
- **ULA** (fd00::/8, RFC 4193): private, not routed on the internet, stable regardless of ISP.

## Generate a ULA correctly
`fd` + 40 **random** bits = a /48. Never use `fd00::/48` or other "pretty" values; random
global ID makes mergers and VPNs between organisations collision-free.
```bash
printf 'fd%s:%s%s:%s%s::/48\n' $(head -c5 /dev/urandom | od -An -tx1)
```
(Ran in Git Bash and printed e.g. `fd1a:5592:d645::/48`.)

## When ULA helps
- Infrastructure that must not change when the ISP (PA prefix) changes: management,
  loopbacks, internal service VIPs, labs.
- Isolated networks never reaching the internet (OT, storage).

## When ULA hurts
- Hosts with both ULA and GUA: the RFC 6724 default policy table gives `fc00::/7` precedence 3 and
  IPv4 (`::ffff:0:0/96`) precedence 35, so a dual-stack host prefers IPv4 over a ULA destination.
  Windows 11 shows the same table (`netsh interface ipv6 show prefixpolicies`: 35 for
  `::ffff:0:0/96`, 3 for `fc00::/7`). ULA-to-GUA source selection is also often surprising.
- ULA + NPTv6/NAT66 to reach the internet recreates IPv4 NAT problems; avoid.
- Two prefixes per host doubles troubleshooting surface.

## Usual recommendation
Get PI space (or a stable PA /48 per site) and use GUA everywhere, firewalled; use ULA only
for clearly isolated or ISP-independent infrastructure. If PA renumbering is the fear,
automate addressing (DHCPv6-PD, IPAM-driven config) instead of hiding behind ULA.

## Verify
- [ ] ULA prefix randomly generated and recorded in IPAM; host source address selection tested (`netsh interface ipv6 show prefixpolicies` on Windows, `ip -6 route get` on Linux) with a real dual-stack destination.
