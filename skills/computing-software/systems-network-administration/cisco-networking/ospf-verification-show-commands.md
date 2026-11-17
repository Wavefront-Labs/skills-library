---
id: computing-software.systems-network-administration.cisco-networking.ospf-verification-show-commands
name: ospf-verification-show-commands
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, show-ip-ospf, ospf-neighbor, ospf-database, ospf-interface, verification]
level: practitioner
status: draft
description: "Verify an OSPF deployment with the core show commands: process, interface, neighbour, database, border routers and routes, and what healthy output looks like."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-s1.html
  - https://www.cisco.com/c/en/us/support/docs/ip/open-shortest-path-first-ospf/13688-16.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Verifying OSPF

Work from the process down to the routes; each command answers one question.

## 1. Is the process right?
```
show ip ospf
!  Routing Process "ospf 1" with ID 10.0.0.1
!  Number of areas in this router is 2. 1 normal 0 stub 1 nssa
!  It is an area border router
!  SPF schedule delay / Number of external LSA
```
Check router ID (stable loopback), ABR/ASBR role, SPF run counts (a climbing count means churn).

## 2. Which interfaces run OSPF and how?
```
show ip ospf interface brief
!  Interface  PID Area IP Address/Mask  Cost State Nbrs F/C
!  Gi0/1      1   0    10.0.12.1/30     1    P2P   1/1
show ip ospf interface Gi0/1
```
`Nbrs F/C` = full/total neighbours. State `DR`, `BDR`, `DROTH`, `P2P`, `LOOP`. Passive interfaces
appear with no neighbours, which is expected.

## 3. Are adjacencies healthy?
```
show ip ospf neighbor
!  Neighbor ID  Pri State     Dead Time Address   Interface
!  10.0.0.2     0   FULL/  -  00:00:34  10.0.12.2 Gi0/1
show ip ospf neighbor detail | include Neighbor|up for|area
```
FULL on point-to-point and with DR/BDR; `2WAY/DROTHER` between two DROTHERs is normal. Stuck
states: INIT (one-way), EXSTART/EXCHANGE (MTU), 2WAY where FULL expected (network type).

## 4. Is the LSDB complete and consistent?
```
show ip ospf database
show ip ospf database router 10.0.0.2
show ip ospf database summary 10.20.0.0
show ip ospf database external
show ip ospf database database-summary
```
Same area must show identical LSDBs on all routers (compare `database-summary` counts and checksums).

## 5. Border routers and resulting routes
```
show ip ospf border-routers
show ip route ospf
!  O     intra-area   O IA inter-area   O E1/E2 external   O N1/N2 NSSA external
show ip ospf rib          ! OSPF local RIB before selection, IOS XE
```

## Healthy checklist
- [ ] Router ID unique and from a loopback.
- [ ] Every expected neighbour FULL (or 2WAY between DROTHERs) with stable uptime.
- [ ] SPF count not increasing between two checks minutes apart.
- [ ] Expected O / O IA / O E2 routes present with sensible costs.
