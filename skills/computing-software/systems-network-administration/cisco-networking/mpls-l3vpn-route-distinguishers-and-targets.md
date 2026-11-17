---
id: computing-software.systems-network-administration.cisco-networking.mpls-l3vpn-route-distinguishers-and-targets
name: mpls-l3vpn-route-distinguishers-and-targets
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, mpls, l3vpn, route-distinguisher, route-target, mp-bgp, vpnv4, pe-ce, vrf]
level: practitioner
status: docs-checked
description: "Understand route distinguishers versus route targets in BGP/MPLS L3VPN (RFC 4364): VPN-IPv4 addresses, import/export targets, and full-mesh, hub-and-spoke and extranet designs."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4364
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MPLS L3VPN route distinguishers and route targets

## RD vs RT (RFC 4364 sections 4.1-4.3)
| | Route distinguisher | Route target |
|---|---|---|
| What | 8-byte prefix that makes an IPv4 prefix into a 12-byte VPN-IPv4 address | BGP extended community carried as an attribute of the route |
| Purpose | lets BGP carry distinct routes for the same IPv4 prefix used in different VPNs | decides which VRFs a route is distributed to and installed in |
| Count per route | exactly one | one or more |

- An RD is only a number: it does not identify the route's origin or the set of VPNs that get the route. Its sole
  purpose is to allow distinct routes to a common IPv4 prefix. VPN-IPv4 and IPv4 are different address families, so BGP
  never compares them.
- RD encoding: 2-byte type plus 6-byte value. Type 0: 2-byte ASN administrator and 4-byte assigned number. Type 1:
  4-byte IPv4 administrator and 2-byte assigned number. Type 2: 4-byte ASN administrator and 2-byte assigned number.
  BGP ignores this structure when comparing prefixes. Private ASNs and addresses are strongly discouraged as
  administrators.
- A PE can be configured to give all routes toward a CE one RD, or different routes different RDs even to the same CE.
  The same IPv4 prefix with two different RDs gives two routes, so policy can choose which packets use which route
  (the RFC's example is separate intranet and extranet routes to one server).
- Each VRF has Export Targets (attached to routes learned from the site) and Import Targets (used to decide whether a
  route from another PE may go into the VRF). The two sets are distinct and need not match. A route is eligible for a
  VRF only if one of its Route Targets is one of the VRF's Import Targets. Route Targets are not the BGP Communities
  attribute because that has only a 2-byte numbering space.
- Using several RTs on one route scales better than creating more routes with more RDs.
- Route distribution between VRFs in the same PE follows the same RT rules.

## Topologies with RTs
- Full mesh: one RT chosen per VPN, set as both import and export target on each site's VRF and on no other VRF.
- Hub and spoke: two RTs, "Hub" and "Spoke". Hub VRFs export Hub and import Spoke; spoke VRFs import Hub and export
  Spoke.
- Extranet: a site can be in more than one VPN (an intranet and several extranets); the RFC treats intranets and
  extranets alike as VPNs.

## Operating notes
- Route reflectors can be preconfigured with a list of RTs so no single reflector must hold all VPN routes
  (RFC 4364 section 4.3.3).
- If a CE that peers by BGP is allowed to attach RTs, the PE must filter out routes carrying RTs the customer may not
  use.
- IOS XE configuration (`rd`, `route-target`, `address-family vpnv4`, PE-CE BGP) is not covered here: the Cisco guide
  cited earlier returned 404. Use the configuration guide for your release.

## Checked
Date: 2026-11-08. Read: RFC 4364 sections 4.1 through 4.3.1 and 4.3.5, plus section 4.3.3 headlines via search. The
Cisco MPLS L3VPN configuration guide URL returned 404 and was dropped.
Confirmed: every statement above against the RFC text.
Removed: all IOS XE configuration (`vrf definition`, `rd`, `route-target`, `vpnv4` BGP, `as-override`, LDP lines), the
claim that a unique RD per PE per VRF lets route reflectors keep multihomed paths while a shared RD makes the RR pick
one (not in the RFC), the `<PE-loopback>:<vrf-id>` RD convention, and all show/ping verification commands.
Method: documentation only; no commands were run.
