---
id: computing-software.systems-network-administration.cisco-networking.stateful-nat-redundancy
name: stateful-nat-redundancy
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, nat, stateful-nat, nat-ha, box-to-box-redundancy, redundancy-group, hsrp-nat, stateful-failover]
level: practitioner
status: draft
description: "Make IOS XE NAT survive a router failure with box-to-box redundancy groups (RG) and stateful translation sync, versus stateless HSRP-mapped NAT."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-ha.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_nat/configuration/xe-16/nat-xe-16-book/iadnat-b2b-red.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stateful NAT redundancy

## Options
| Method | Translations survive failover? | Notes |
|---|---|---|
| Two routers with HSRP, NAT on each (`redundancy <hsrp-name>` mapping for static NAT) | no for dynamic | sessions reset; inside global addresses move with HSRP |
| Box-to-box redundancy groups (IOS XE, ASR1000/ISR4000/C8000) | yes | translation and firewall state synced over a control/data link |
| Legacy SNAT (Stateful NAT with HSRP) | yes | deprecated in IOS XE; do not deploy |

## Box-to-box redundancy group (outline)
```
redundancy
 application redundancy
  group 1
   priority 150 failover threshold 140
   preempt
   control GigabitEthernet0/0/3 protocol 1
   data GigabitEthernet0/0/3
   track 10 shutdown
interface GigabitEthernet0/0/1        ! inside
 ip nat inside
 redundancy rii 100
 redundancy group 1 ip 10.0.0.1 exclusive   ! virtual inside gateway
interface GigabitEthernet0/0/0        ! outside
 ip nat outside
 redundancy rii 101
 redundancy group 1 ip 203.0.113.1 exclusive
ip nat pool OUT 203.0.113.10 203.0.113.20 prefix-length 24
ip nat inside source list NAT-ACL pool OUT redundancy 1 mapping-id 10
```
Both routers need identical NAT config with the same `mapping-id`; the RII (redundancy interface
identifier) pairs interfaces between boxes.

## Gotchas
- The data link must have enough bandwidth for state sync; put it on a dedicated port.
- Asymmetric routing (return traffic hitting the standby) breaks unless the outside network
  routes to the RG virtual address only, or asymmetric routing support is configured.
- PAT with interface overload cannot be synced; use a pool on a shared subnet.
- Upgrade both boxes to the same release; RG peers with mismatched versions may not sync.

## Verify
```
show redundancy application group 1           ! ACTIVE/STANDBY, peer state
show ip nat translations total                ! counts similar on both boxes
show ip nat redundancy 1
```
- [ ] Long-lived TCP session (SSH) survives reload of the active router.
