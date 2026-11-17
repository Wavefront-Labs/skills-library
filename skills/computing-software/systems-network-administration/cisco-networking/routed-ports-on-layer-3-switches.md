---
id: computing-software.systems-network-administration.cisco-networking.routed-ports-on-layer-3-switches
name: routed-ports-on-layer-3-switches
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, layer-3-switch, routed-port, no-switchport, ip-routing, svi, point-to-point, routed-access, slash-31, ipv6-unicast-routing, vlan, access-port]
level: practitioner
status: draft
description: "Configure routed ports on Catalyst layer 3 switches: no switchport, ip routing, /31 point-to-point uplinks, SVI vs routed port trade-offs and routed-access design checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_interface_characteristics.html
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/routed-ex.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Routed ports on layer 3 switches

A routed port is a physical switch interface that behaves like a router interface: no VLAN, no
STP, no MAC learning for transit, its own IP address.

## Configure
```
ip routing                         ! off by default on many Catalyst models
ipv6 unicast-routing
!
interface TenGigabitEthernet1/1/1
 description to-DIST1 Te1/0/1
 no switchport
 ip address 10.255.0.1 255.255.255.254    ! /31 per RFC 3021
 ipv6 address 2001:db8:ff::/127
 ip ospf network point-to-point
 no ip proxy-arp
 load-interval 30
```
`no switchport` wipes any Layer 2 config on the port and briefly bounces it.

## SVI vs routed port
| | SVI (interface VlanX) | Routed port |
|---|---|---|
| Use | gateway for hosts on a VLAN, multiple ports | single point-to-point uplink |
| STP | runs in the VLAN; slower failure detection | none; link down = route withdrawn immediately |
| Up/down | up while any port in VLAN is up (autostate) | follows the physical link |
| Convergence | depends on STP and timers | sub-second with BFD/fast hello |

For switch-to-switch uplinks in routed-access or L3 distribution designs, routed ports (or a
Layer 3 Port-channel) are faster and simpler than a transit VLAN with SVIs.

## Check commands
```
show ip interface brief | ex unassigned
show interfaces Te1/1/1 switchport     ! "Switchport: Disabled"
show ip route connected
ping 10.255.0.0 source Te1/1/1
```

## Gotchas
- Forgetting `ip routing` gives connected routes only; the switch acts as a host and drops
  transit traffic.
- `/31` works on IOS XE and most peers; some old third-party gear or firewalls need `/30`.
- SVI autostate: an SVI stays up if any access/trunk port in the VLAN is up, which can
  blackhole traffic during an uplink failure. Use routed ports for uplinks, or
  `switchport autostate exclude` on ports that should not keep the SVI up.
- MTU: routed ports use `mtu` / `ip mtu` per interface, while L2 ports use `system mtu`.
  Mismatched IP MTU on OSPF neighbours stalls at EXSTART.

## Verify
- [ ] `show interfaces <port> switchport` reports disabled.
- [ ] Routing adjacency forms over the routed port; `show ip route` learns remote prefixes.
- [ ] Shutting the link removes the route immediately (`show ip route` changes, no STP wait).
