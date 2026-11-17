---
id: computing-software.systems-network-administration.cisco-networking.ospfv3-ipv6-address-families
name: ospfv3-ipv6-address-families
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, ospfv3, ospf, ipv6, ipv6-routing, link-local, rfc5340, instance-id]
level: practitioner
status: docs-checked
description: "OSPFv3 per RFC 5340: per-link operation over link-local addresses, LSA type codes, link and intra-area-prefix LSAs, Instance ID, 32-bit router IDs, and IPsec authentication."
sources:
  - https://www.rfc-editor.org/rfc/rfc5340
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPFv3 for IPv6 (RFC 5340)

Protocol-level behaviour. The IOS XE configuration chapter was a 404 when checked, so no CLI is given: use your
platform's OSPFv3 guide for how to enable it per interface and to set a router ID.

## What changed from OSPFv2
- OSPF for IPv6 runs per link, not per subnet. Multiple IPv6 prefixes can be on one link.
- Router IDs, area IDs and LSA Link State IDs stay 32 bits; they can no longer be assigned as IPv6 addresses. A router
  therefore needs a 32-bit router ID configured when it has no IPv4 address to derive one from (inference from the
  32-bit rule: IPv6 addresses cannot serve as IDs; check your platform for the error it raises). 0.0.0.0 is reserved.
- Neighbours are always identified by Router ID, on every network type.
- Router-LSAs and network-LSAs carry no addresses, only topology, so the topology is independent of addressing.
  Router interface information may span multiple router-LSAs; receivers concatenate them for SPF.
- Prefixes are written as prefix plus prefix length; the default route is a prefix of length 0.
- The Options field moved out of the LSA header (now 24 bits, in bodies of router, network, inter-area-router and
  link LSAs); the LSA type is 16 bits whose upper bits encode flooding scope and handling of unknown types.
- New Options bits: R-bit and V6-bit. R clear: take part in topology distribution but do not forward transit traffic.
  V6 clear: do not forward IPv6 datagrams.
- Type 3 summary-LSAs are now inter-area-prefix-LSAs, type 4 are inter-area-router-LSAs.

## LSA types
| LS type | Name | Notes |
|---|---|---|
| 0x2001 | Router-LSA | area scope |
| 0x2002 | Network-LSA | area scope; Link State ID is the DR's Interface ID |
| 0x2003 | Inter-area-prefix-LSA | |
| 0x2004 | Inter-area-router-LSA | |
| 0x4005 | AS-external-LSA | |
| 0x2007 | NSSA-LSA | |
| 0x0008 | Link-LSA | link-local flooding scope, never beyond the link |
| 0x2009 | Intra-area-prefix-LSA | carries the prefixes of the router or the transit network |

A link-LSA gives the router's link-local address to the other routers on the link (used for next hops), lists the IPv6
prefixes to associate with the link, and supplies Options bits for the network-LSA. The network-LSA Options are the OR
of those in the link-LSAs.

## Link-local addresses
- Every router must have link-local addresses on its links; OSPF packets use the interface's link-local address as
  source (except virtual links, which use a global address). Next hops are other routers' link-local addresses, so
  routes whose next hop is FE80::/10 on an interface are expected.
- Link-local addresses must not be advertised in inter-area-prefix, AS-external, NSSA or intra-area-prefix LSAs.
- Multicast: AllSPFRouters FF02::5 (Hellos always go there) and AllDRouters FF02::6.

## Instance ID and authentication
- The packet header carries an Instance ID so that several OSPF instances can run on one link (for example one link in
  two areas). It affects only packet reception; a packet is accepted when Area ID and Instance ID match the interface.
- Authentication was removed from the protocol (no AuType/Authentication fields). OSPFv3 relies on IPv6 AH and ESP
  (as described in a separate document) for integrity and optional confidentiality.

## Verify
- [ ] Neighbours reach Full; next hops are link-local addresses on the right interface.
- [ ] Router ID is unique and set explicitly if no IPv4 address exists.
- [ ] Authentication, if used, is IPsec-based and configured consistently at both ends.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read RFC 5340 sections 2.1-2.11 (per-link operation, instance ID,
link-local use, authentication changes, LSA format changes, neighbour identification), 4.4.3 LSA type values and
purposes, and the multicast address definitions. Removed as unconfirmed: all IOS XE syntax (Cisco page is a 404), the
address-family (IPv4 over OSPFv3, RFC 5838) material, reference-bandwidth, passive-interface, show commands and
the RFC 7166 trailer authentication remark, none of which are in RFC 5340.
