---
id: computing-software.systems-network-administration.cisco-networking.ipv6-neighbor-discovery-troubleshooting
name: ipv6-neighbor-discovery-troubleshooting
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ipv6, neighbor-discovery, ndp, neighbor-solicitation, neighbor-advertisement, router-advertisement, nd-cache, icmpv6, incomplete]
level: practitioner
status: docs-checked
description: "Troubleshoot IPv6 Neighbor Discovery using RFC 4861: ICMPv6 message types, neighbour cache states, Hop Limit 255 rule, protocol constants and what to check."
sources:
  - https://datatracker.ietf.org/doc/html/rfc4861
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IPv6 Neighbor Discovery troubleshooting

## Message types (RFC 4861)
ICMPv6 Router Solicitation 133, Router Advertisement 134, Neighbor Solicitation 135, Neighbor Advertisement 136,
Redirect 137. All are sent with IP Hop Limit 255, and receivers check for 255: a packet that has crossed a router
would have a lower value, so ND packets cannot originate from off-link.

## Neighbour cache states
| State | Meaning |
|---|---|
| INCOMPLETE | address resolution in progress; link-layer address not yet known |
| REACHABLE | known reachable recently (tens of seconds) |
| STALE | no longer known reachable; no probe until traffic is sent (normal) |
| DELAY | traffic recently sent; probing is delayed to let upper layers confirm reachability |
| PROBE | unicast Neighbor Solicitations are being sent to verify reachability |

Per the RFC's state table, an INCOMPLETE entry whose retransmit timer expires after the maximum number of
solicitations is discarded, and a PROBE entry is discarded the same way. So a neighbour that never answers means
Neighbor Solicitations are not getting an answer: check VLAN/Layer 2 path and ICMPv6 filtering.

## Protocol constants (RFC 4861 section 10)
MAX_MULTICAST_SOLICIT 3 and MAX_UNICAST_SOLICIT 3 transmissions, REACHABLE_TIME 30,000 ms, RETRANS_TIMER 1,000 ms,
DELAY_FIRST_PROBE_TIME 5 s, RTR_SOLICITATION_INTERVAL 4 s, MAX_RTR_SOLICITATIONS 3. Vendors may differ in
implementation defaults; read the device's own output.

## Hosts get no address or default gateway
1. Confirm the router sends Router Advertisements (type 134) on the link; capture on the host and filter ICMPv6
   type 134.
2. Check the RA contents: prefix, on-link and autonomous flags, M and O flags, and Router Lifetime. A Router
   Lifetime of zero means the router is not to be used as a default router.
3. See ipv6-router-advertisement-tuning for the RA variables.

## Filtering mistakes
ND is carried in ICMPv6; ACLs or firewalls that drop ICMPv6 types 133-137 break address resolution and router
discovery. Allow them (with Hop Limit untouched) on every ND-carrying link.

## Checked
Checked 2026-11-08 against RFC 4861: message type numbers (section 4.x and the type table), Hop Limit 255
requirement, neighbour cache states (section 5.1 and 7.3.2), state table, and constants (section 10). Removed:
Cisco `show` and `ipv6 nd` command examples, DAD/`[DUP]` handling (RFC 4862, not read), RA Guard configuration,
implicit-permit ACL behaviour, MLD snooping remarks, and ndisc6 tooling; the Cisco ND configuration page returned 404.
Method: documentation only; no commands were run.
