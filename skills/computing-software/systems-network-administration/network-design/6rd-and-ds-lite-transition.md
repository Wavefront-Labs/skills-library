---
id: computing-software.systems-network-administration.network-design.6rd-and-ds-lite-transition
name: 6rd-and-ds-lite-transition
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, 6rd, ds-lite, ipv6-transition, aftr, b4, cgnat]
level: practitioner
status: docs-checked
description: "Recognise and support ISP IPv6 transition mechanisms 6rd and DS-Lite: how each tunnels, CPE configuration, MTU impact and why DS-Lite breaks inbound port forwarding."
sources:
  - https://www.rfc-editor.org/rfc/rfc5969
  - https://www.rfc-editor.org/rfc/rfc6333
  - https://www.rfc-editor.org/rfc/rfc6334
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 6rd and DS-Lite

## 6rd (RFC 5969): IPv6 over an IPv4-only access network
- The CPE derives its IPv6 delegated prefix from the ISP's 6rd prefix and (part of) its own IPv4 address, and tunnels
  IPv6 across the IPv4 network to a 6rd Border Relay (BR).
- Configuration parameters include the 6rd prefix and length, `IPv4MaskLen` (the number of high-order IPv4 bits that
  are identical across the 6rd domain) and the BR address. DHCPv4 option code **212** (`OPTION_6RD`) carries them.
- The delegated prefix follows the CE's IPv4 address, so an IPv4 renumbering event renumbers the customer's IPv6.
- MTU: the RFC suggests the tunnel MTU might be set to 1480 bytes absent better information; advertise it and clamp MSS.

## DS-Lite (RFC 6333): IPv4 over an IPv6-only access network
- The CPE (B4) tunnels IPv4 in IPv6 to the AFTR, which performs carrier-grade IPv4-IPv4 NAT; customers share the AFTR's
  public addresses.
- The AFTR name is delivered in DHCPv6 option **64** (`OPTION_AFTR_NAME`, RFC 6334).
- The well-known range 192.0.0.0/29 is reserved for DS-Lite; 192.0.0.2 is reserved for the B4 element.
- Tunnelling over IPv6 reduces the effective MTU, and path MTU discovery is not a reliable fix: clamp TCP MSS (the RFC
  discusses MSS clamping).
- Customers have no public IPv4 of their own, so inbound IPv4 port forwarding and hosting are constrained; RFC 6333
  section 8.5 covers port forwarding. Options are IPv6 for inbound, an ISP-provided public IPv4 where offered, or a
  relay.

## Diagnosing a site on one of these
- Router status shows only an IPv6 WAN address and a 192.0.0.x IPv4 address: DS-Lite.
- A public-IP lookup returns an address that is not on the router: carrier-grade NAT.
- Large IPv4 transfers stall while small ones work: MTU or MSS problem in the tunnel.

## Verify
- [ ] Site requirements (inbound access, VPN headend) checked against the ISP mechanism before ordering; MSS clamping set
  to match the tunnel overhead.

## Checked
2026-10-28. Confirmed in RFC 5969, RFC 6333 and RFC 6334: 6rd BR and prefix derivation, `IPv4MaskLen`, option 212,
renumbering, 1480 MTU suggestion, DS-Lite AFTR and CGN, option 64, 192.0.0.0/29 and 192.0.0.2, MTU and MSS discussion.
Removed as unconfirmed: IP protocol numbers 41 and 4, the 1460 and 1420 figures, pricing remark on public IPv4,
geolocation and reputation claim.
Method: documentation only; no commands were run.
