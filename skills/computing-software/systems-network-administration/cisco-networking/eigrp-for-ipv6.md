---
id: computing-software.systems-network-administration.cisco-networking.eigrp-for-ipv6
name: eigrp-for-ipv6
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, eigrp, eigrp-ipv6, eigrp-named-mode, address-family-ipv6, ipv6-routing, router-id]
level: practitioner
status: draft
description: "Run EIGRP for IPv6 in named mode (or classic ipv6 router eigrp): router ID, per-interface enablement, link-local neighbours and verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_eigrp/configuration/xe-16/ire-xe-16-book/ire-ipv6.html
  - https://datatracker.ietf.org/doc/html/rfc7868
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# EIGRP for IPv6

## Named mode (preferred)
```
ipv6 unicast-routing
router eigrp CORP
 address-family ipv6 unicast autonomous-system 100
  eigrp router-id 10.255.0.1          ! 32-bit ID required; no IPv4 address = no auto RID
  af-interface default
   passive-interface
  exit-af-interface
  af-interface GigabitEthernet0/0
   no passive-interface
  exit-af-interface
  topology base
   maximum-paths 4
  exit-af-topology
```
In named mode IPv6 address family, **all IPv6-enabled interfaces join automatically**; control with
`af-interface ... shutdown` or passive.

## Classic mode
```
ipv6 router eigrp 100
 eigrp router-id 10.255.0.1
 no shutdown                          ! older releases start shut
interface GigabitEthernet0/0
 ipv6 eigrp 100
```

## Behaviour
- Hellos to FF02::A from link-local sources; neighbours are identified by link-local addresses.
- No `network` statements, no auto-summary.
- Same K values and AS on both sides; authentication via `af-interface ... authentication mode hmac-sha-256`.

## Verify
```
show ipv6 eigrp neighbors
show ipv6 eigrp topology
show ipv6 route eigrp
show eigrp address-family ipv6 interfaces
```
- [ ] Neighbours shown with FE80:: addresses on the expected interfaces.
- [ ] Router ID set explicitly (IPv6-only boxes otherwise fail to start the process).
