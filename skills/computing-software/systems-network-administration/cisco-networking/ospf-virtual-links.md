---
id: computing-software.systems-network-administration.cisco-networking.ospf-virtual-links
name: ospf-virtual-links
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, virtual-link, area-0, transit-area, discontiguous-backbone, ospf-multi-area, gre-tunnel]
level: practitioner
status: docs-checked
description: "Use OSPF virtual links to attach a remote area or heal a split backbone: configure on both ABRs via the transit area, its limits, and the GRE alternative."
sources:
  - https://www.rfc-editor.org/rfc/rfc2328#section-15
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/47866-ospfdb7.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF virtual links

All areas in an OSPF autonomous system should be physically connected to area 0. Where that is not possible, a virtual
link connects an area to the backbone through a non-backbone area, or joins two parts of a partitioned backbone.
The area it crosses is the transit area; it must have full routing information and cannot be a stub area.

## Properties (RFC 2328)
- A virtual link is configured between two area border routers that attach to a common area (the transit area), and
  is identified by the other endpoint's Router ID. A router with a virtual link must itself be an ABR.
- Virtual links are part of the backbone and behave like unnumbered point-to-point networks; they use the transit
  area's intra-area routing to forward packets, and come up or down as the transit area's shortest-path tree is built.
- Each has an IP interface address, discovered during the routing-table build, used as source for packets sent over it.
- Hello packets over a virtual link are unicast to the other end.
- Virtual links cannot be configured through stub areas.

## Configure (Cisco example pattern)
The Cisco page configures it on both ends with the transit area and the far router's router ID, not an interface
address:
```
! R1, ABR between area 0 and transit area 10, router ID 10.0.0.1
router ospf 1
 area 10 virtual-link 10.0.0.3
! R3, ABR between area 10 and the remote area, router ID 10.0.0.3
router ospf 1
 area 10 virtual-link 10.0.0.1
```
The link starts down: LSAs in the transit area must flood and SPF must run so each end can reach the other's router
ID through it. Once adjacent, the remote router counts itself an ABR because it now has a link in area 0 and creates
summary LSAs in both areas; if the link is misconfigured it does not, and the remote area's prefixes are not
advertised. LSAs learned over the link carry the DoNotAge option because the link is treated like a demand circuit.

## Virtual link versus GRE tunnel in area 0 (Cisco page)
- Virtual link: routing updates are tunnelled, data is sent natively with no tunnel overhead, and the transit area
  cannot be a stub area (stub routers lack external routes, so externally destined packets are mis-routed).
- GRE tunnel: all traffic is encapsulated (overhead on every packet), but the tunnel can cross a stub area.

## Verify
Use the OSPF database commands the Cisco page lists, such as `show ip ospf database` and
`show ip ospf database router`, and look for "Link connected to: a Virtual Link" in the router LSA of each end. Check
that the remote area's summary routes appear in area 0.

## Checked
Checked 2026-11-08 against RFC 2328 (virtual link definition, stub restriction, unicast hellos, interface address) and
the Cisco "Configure OSPF Connection in a Virtual Link Environment" page (configuration pattern, behaviour, GRE
comparison, DoNotAge). Removed: virtual-link authentication commands, `show ip ospf virtual-links` sample output,
the NSSA restriction, the "no DR election" claim and the advice to treat links as temporary with a removal date.
Method: documentation only; no commands were run.
