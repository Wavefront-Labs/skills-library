---
id: computing-software.systems-network-administration.network-design.directed-broadcast-and-wake-on-lan
name: directed-broadcast-and-wake-on-lan
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, directed-broadcast, wake-on-lan, magic-packet, smurf-attack, ip-helper]
level: practitioner
status: draft
description: "Wake machines across subnets safely: magic packet format, why directed broadcasts are off by default, scoped ip directed-broadcast with ACLs, and WOL proxy alternatives."
sources:
  - https://www.rfc-editor.org/rfc/rfc2644
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/13702-wol-catos.html
  - https://learn.microsoft.com/en-us/intune/configmgr/core/clients/deploy/configure-wake-on-lan
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Directed broadcast and Wake-on-LAN

## Magic packet
6 bytes of `FF` followed by the target MAC repeated 16 times (102 bytes), usually in UDP to port
9 (or 7). The NIC listens while powered down, so the packet must reach the **sleeping host's L2
segment** as a broadcast (the switch has no MAC entry after aging).

## Directed broadcast
A packet to a remote subnet's broadcast address (e.g. 10.20.0.255) that the last-hop router
converts into an L2 broadcast. RFC 2644 made routers drop these by default (smurf amplification).
Enable narrowly:
```
access-list 110 permit udp host 10.1.1.50 any eq 9    ! only the management server
interface Vlan20
 ip directed-broadcast 110
```
Also allow UDP/9 from the WOL server through any firewall in between.

## Alternatives
- `ip helper-address 10.20.0.255` + `ip forward-protocol udp 9` on the source-side SVI.
- A WOL proxy/agent per subnet (ConfigMgr client peer wake-up, a small agent or Raspberry Pi).
- Out-of-band (iDRAC/iLO/Intel AMT) for servers and managed desktops.

## Host prerequisites
- BIOS/UEFI: Wake on LAN / Power on by PCI-E enabled; ErP/EuP deep sleep disabled.
- OS: NIC "Allow this device to wake the computer" and "Only allow a magic packet". Windows Fast
  Startup can stop WOL from S5; disable it if needed.
- Linux: `ethtool eth0 | grep Wake-on` should show `g`; set `ethtool -s eth0 wol g`.
- Wi-Fi clients generally cannot be woken this way.

## Test
```
wakeonlan -i 10.20.0.255 00:11:22:33:44:55
tcpdump -i eth0 -n 'udp port 9'   # on a host in the target VLAN
```

## Verify
- [ ] Packet capture on the target VLAN sees the magic packet; a powered-off test host wakes; directed broadcast is accepted only from the WOL source.
