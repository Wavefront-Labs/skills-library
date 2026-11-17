---
id: computing-software.systems-network-administration.cisco-networking.multicast-troubleshooting-mroute-mtrace
name: multicast-troubleshooting-mroute-mtrace
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, multicast, multicast-troubleshooting, mtrace, mroute, pim, igmp, rpf]
level: practitioner
status: draft
description: "Troubleshoot a multicast stream end to end: receiver IGMP join, last-hop (*,G) and (S,G) state, RPF and RP checks, mtrace, and packet counters along the tree."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/ip-multicast/13726-35.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipmulti_pim/configuration/xe-16/imc-pim-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Multicast troubleshooting

Work from the receiver toward the source (the direction PIM joins travel).

## 1. Receiver side
```
show ip igmp groups 239.1.1.10
show ip igmp snooping groups vlan 20        ! on the access switch
show ip igmp interface Vlan20 | include querier|version
```
No group: host not sending IGMP reports (app, OS firewall), wrong VLAN, or no querier on the VLAN
(snooping switches then age out groups after ~260 s; streams stop after a few minutes).

## 2. Last-hop router state
```
show ip mroute 239.1.1.10
!  (*, 239.1.1.10), RP 10.0.0.100, flags: SJC
!    Incoming interface: Te1/0/1, RPF nbr 10.0.12.1
!    Outgoing interface list: Vlan20, Forward/Sparse
!  (10.50.0.5, 239.1.1.10), flags: JT
!    Incoming interface: Te1/0/2, RPF nbr 10.0.13.1
```
- No (*,G): IGMP did not reach PIM (PIM not enabled on the receiver SVI, or the router is not the
  DR).
- (*,G) but no (S,G): source traffic never reached the RP or the RP is unknown/wrong.
- Incoming interface Null: RPF failure.

## 3. RPF and RP checks
```
show ip rpf 10.50.0.5          ! must point at the interface traffic actually arrives on
show ip pim rp mapping 239.1.1.10
show ip pim neighbor
```
RPF failure happens when unicast routing to the source prefers a different interface than the
multicast path (asymmetric routing, PIM not enabled on the preferred interface). Fix routing or add
`ip mroute` static RPF entries.

## 4. Trace the path
```
mtrace 10.50.0.5 10.20.0.15 239.1.1.10      ! source, receiver, group
```
Shows each hop's incoming interface, RPF neighbour, forwarding code (e.g. `RPF Interface`,
`No route`, `Wrong interface`, `Prune sent upstream`).

## 5. Is it forwarding?
```
show ip mroute 239.1.1.10 count             ! packets and rate per (S,G), RPF failed counter
show ip mfib 239.1.1.10                     ! hardware forwarding entries
```
Run the count twice; the forwarding packet count must increase at each hop.

## Gotchas
- TTL: many apps send multicast with TTL 1; it dies at the first router.
- PIM must be enabled on every interface in the path including the source's first-hop SVI.
- Firewalls in the path need multicast routing enabled explicitly.

## Verify
- [ ] Receiver gets the stream; every hop shows (S,G) with increasing packet counts and no RPF fails.
