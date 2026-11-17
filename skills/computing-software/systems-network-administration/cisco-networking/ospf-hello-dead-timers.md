---
id: computing-software.systems-network-administration.cisco-networking.ospf-hello-dead-timers
name: ospf-hello-dead-timers
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ospf, ospf-timers, ospf-hello-interval, dead-interval, fast-hello, adjacency]
level: practitioner
status: docs-checked
description: "Set and troubleshoot OSPF hello and dead intervals: defaults, mismatches that block adjacency, fast hellos with minimal dead-interval, and when to use BFD."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/configuration/xe-16/iro-xe-16-book/iro-fast-hello.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/iproute_ospf/command/iro-cr-book/ospf-i1.html
  - https://www.rfc-editor.org/rfc/rfc2328
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OSPF hello and dead timers

## Defaults
| Network type | Hello |
|---|---|
| Ethernet | 10 s |
| non-broadcast | 30 s |

The dead interval defaults to 4 x the hello interval (Cisco `ip ospf hello-interval` reference).
Check the reference for your release for other network types.

## Mismatch blocks the adjacency
RFC 2328 requires HelloInterval and RouterDeadInterval to be the same on all routers attached to a
common network. A mismatch means no neighbour forms.
```
show ip ospf interface Gi0/1
debug ip ospf hello          ! reports mismatched hello parameters
```
The classic cause is one side Ethernet (10/40) and the other non-broadcast (30/120), or a template
applied to one side only.

## Tuning
```
interface Gi0/1
 ip ospf hello-interval 3
 ip ospf dead-interval 12
```
Fast hello (sub-second detection without BFD): `ip ospf dead-interval minimal hello-multiplier N`
sets the dead interval to 1 second and sends N hellos per second (Cisco "OSPF Support for Fast
Hello Packets").
```
interface Gi0/1
 ip ospf dead-interval minimal hello-multiplier 4
```

## Prefer BFD for fast detection
Hellos are processed by the control plane and compete with everything else; sub-second hellos on
many interfaces burden the CPU and can false-trip under load. BFD is lighter:
```
router ospf 1
 bfd all-interfaces
interface Gi0/1
 bfd interval 50 min_rx 50 multiplier 3
```
Keep OSPF timers at defaults and let BFD signal failures.

## Gotchas
- Through a provider L2 service, the link stays up when the far end dies; the dead interval (or BFD)
  is the only detector. That is where tuning matters.
- Changing timers on a live link drops the adjacency until both ends match. Change both in one
  window.

## Verify
- [ ] `show ip ospf neighbor` shows FULL and Dead Time counting down from the configured value.
- [ ] Failover test meets the target detection time.

## Checked
2026-10-31. Confirmed in the Cisco OSPF command reference (`ip ospf hello-interval`: 10 s Ethernet,
30 s non-broadcast; dead = 4 x hello), the Cisco fast-hello page (`dead-interval minimal
hello-multiplier`, 1 second dead interval), the BGP command reference example for the `bfd interval
50 min_rx 50 multiplier 3` syntax, `bfd all-interfaces` under OSPF, and RFC 2328 (hello and dead
intervals must match). Removed: point-to-point and point-to-multipoint defaults, the quoted debug
message text, the multi-vendor note and the CPU/hardware-offload claims, which no fetched page confirms.
Method: documentation only; no commands were run.
