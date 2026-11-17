---
id: computing-software.systems-network-administration.network-design.ipv6-address-plan-nibble-boundaries
name: ipv6-address-plan-nibble-boundaries
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, ipv6, ipv6-address-plan, nibble-boundary, prefix-delegation, slash-48, slash-64, addressing-plan]
level: practitioner
status: verified
description: "Build an IPv6 address plan on nibble boundaries: /48 per site, /56 or /64 allocations, encoding site, function and VLAN in hex digits, and leaving room to grow."
sources:
  - https://www.ripe.net/publications/docs/ripe-690
  - https://www.rfc-editor.org/rfc/rfc6177
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# IPv6 address plan on nibble boundaries

IPv6 planning is about structure, not conservation. Every subnet is a /64 (SLAAC needs it);
what you plan is the bits between your allocation and /64.

## Allocation sizes
| Prefix | Use |
|---|---|
| /32 | ISP/LIR-scale allocation (check your RIR's policy for minimum sizes) |
| /48 | one site (65 536 /64s); RIPE-690 offers /48 for every end-user, or /48 for business and /56 for residential, and strongly discourages anything longer than /56; RFC 6177 dropped RFC 3177's fixed /48 default |
| /56 | small site or residential customer (256 /64s) |
| /64 | one subnet / VLAN |
| /127 | point-to-point links (RFC 6164); reserve a /64 per link anyway |
| /128 | loopbacks, from one dedicated /64 |

## Nibble boundaries
Each hex digit is 4 bits. Split on multiples of 4 (/36, /40, /44, /48, /52, /56, /60, /64) so
boundaries line up with the digits you read. `2001:db8:12:3400::/56` is readable; a /57 splits
a digit and makes reverse DNS (ip6.arpa is per nibble) and ACLs painful.

## Encode meaning in the digits
Example enterprise `2001:db8:a000::/36`:
```
2001:db8:a R SS : F VVV ::/64
  R  = region (1 hex digit)      -> /40
  SS = site (2 digits)           -> /48 per site
  F  = function (0 infra, 1 users, 2 voice, 3 servers, f mgmt)  -> /52
  VVV= VLAN or index             -> /64
```
`2001:db8:a103:1010::/64` = region 1, site 03, users, VLAN 010. Matching the IPv4 VLAN ID
in the last digits helps operators (the example decodes and nests correctly: that /64 sits inside `2001:db8:a103::/48`, which sits inside the `/36`).

## Rules
- Do not reuse IPv4 scarcity habits: no /120 LANs, no tight packing.
- Reserve space for growth at each level (leave half the region/site digits unused).
- Document in IPAM (NetBox) before deploying; record the scheme itself, not just prefixes.
- Summarise per site/region in routing; the plan should make one prefix per site possible.

## Verify
- [ ] Every boundary on a nibble; each site summarises to one /48; plan recorded in IPAM.
