---
id: computing-software.networking-hardware-and-wireless.check-point.gaia-interfaces-and-routing
name: gaia-interfaces-and-routing
category: computing-software
field: networking-hardware-and-wireless
product: check-point
tags: [networking-hardware-and-wireless, check-point, gaia-interfaces, bond, static-route]
level: practitioner
status: draft
description: "Configure interfaces, VLAN subinterfaces, bonds and static routes in Gaia clish with save and verification."
sources:
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_Gaia_AdminGuide/Default.htm
  - https://sc1.checkpoint.com/documents/R81.20/WebAdminGuides/EN/CP_R81.20_CLI_ReferenceGuide/Default.htm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gaia interfaces, bonding and static routes

```
add bonding group 1
add bonding group 1 interface eth2
add bonding group 1 interface eth3
set bonding group 1 mode 8023AD lacp-rate slow xmit-hash-policy layer3+4
set interface bond1 ipv4-address 10.1.20.1 mask-length 24
add interface eth1 vlan 100
set interface eth1.100 ipv4-address 10.1.30.1 mask-length 24
set static-route 192.168.0.0/16 nexthop gateway address 10.1.10.200 on
save config
show route static
```
- Bond modes: `8023AD` (LACP), `round-robin`, `active-backup`, `xor`. Under ClusterXL, bond (and bond failover) interacts with cluster state; configure the same slave interfaces and mode on all members.
- Create bonds before assigning IP to the slave interface (slaves must have no address).
- Interface names in SmartConsole must match those on the gateway (`Get Interfaces`) so topology and anti-spoofing line up.
- Check speed and duplex with `ethtool eth1`; use `set interface eth1 link-speed 1000M/full` rather than leaving mismatches (autoneg should be on both sides).
- Gotcha: management interface changes (`set management interface`) alter the SIC IP; re-establish trust if the management server sees a different address.

Verify: `show interfaces all`, `cat /proc/net/bonding/bond1`, `ip -s link show eth1` for error counters and `ping -I eth1 <gw>`.
