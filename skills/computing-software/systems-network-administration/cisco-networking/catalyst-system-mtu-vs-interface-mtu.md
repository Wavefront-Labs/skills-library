---
id: computing-software.systems-network-administration.cisco-networking.catalyst-system-mtu-vs-interface-mtu
name: catalyst-system-mtu-vs-interface-mtu
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, system-mtu, interface-mtu, jumbo-frames, ip-mtu, ipv6-mtu]
level: practitioner
status: docs-checked
description: "Catalyst 9300 IOS XE 17.9 MTU: global system mtu vs per-interface ip mtu and ipv6 mtu, their ranges, default 1500, and how to check the applied values."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_system_mtu.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# System MTU vs protocol MTU on Catalyst 9300 (IOS XE 17.9)

## Knobs and ranges
| Command | Mode | Effect and range (per the 17.9 chapter) |
|---|---|---|
| `system mtu <bytes>` | global | affects all ports of the switch or stack; 1500 to 9198 |
| `ip mtu <bytes>` | interface | IPv4 MTU; 832 up to 1500 per the chapter's table |
| `ipv6 mtu <bytes>` | interface | IPv6 MTU; 1280 up to the system jumbo MTU value |

- The default MTU for payload in Ethernet frames on all interfaces is 1500 bytes; the maximum system MTU is 9198.
- The IP and IPv6 MTU values shown are the applied value, not the configured value, and the upper limit is based on the currently applied system MTU.
- From IOS XE Amsterdam 17.3.x the minimum IPv6 system MTU is fixed at 1280 (RFC 8200).
- Protocol-specific MTU under a routed interface is how the chapter says to override system MTU values on routed interfaces.

## Procedure from the chapter
```
configure terminal
 system mtu 1900
 end
copy running-config startup-config
show system mtu
```
Protocol-specific override on a routed interface:
```
configure terminal
 interface gigabitethernet0/0
  ip mtu 900
  ipv6 mtu 1286
  end
show system mtu
```
(The chapter's own examples use 1600/1900 for system MTU and 900/1286 for protocol MTU; they are illustrations.)

- Step 3 of the system procedure describes `system mtu` as changing the MTU for all Gigabit Ethernet and 10-Gigabit Ethernet interfaces.
- `show ip mtu` shows the correct MTU value for interfaces, including loopbacks; `show system mtu` verifies the setting.
- A separate chapter, "Configuring Per-Port MTU", covers per-port MTU; this skill does not cover it. Look it up in the same configuration guide.

## Not covered by the cited page
Reload requirements, behaviour on older Catalyst models (2960/3560/3750/3850), OSPF neighbour MTU checks and DF-bit ping tests are outside the cited chapter. Verify them against the platform's own guide before relying on them.

## Verify
- [ ] `show system mtu` reports the value you set.
- [ ] `show ip mtu` shows the applied IP MTU for each routed interface.

## Checked
Date: 2026-11-08. Read in full: Configuring System MTU chapter, Catalyst 9300 IOS XE Cupertino 17.9.x Interface and Hardware Components guide (about 7.5k characters).
Confirmed: default 1500 and maximum 9198, `system mtu` range 1500 to 9198 affecting all ports, `ip mtu` range 832 to 1500, `ipv6 mtu` range 1280 to system jumbo MTU, applied-vs-configured note, IPv6 minimum 1280 from 17.3.x, both procedures, `show system mtu`, `show ip mtu`.
Removed: the per-interface `mtu` override example and the "Cat 9000 applies without reload" claim (not on the page), SVI `ip mtu <= system mtu` as stated, the legacy `system mtu jumbo`/`routing` claims, OSPF EXSTART and `ip ospf mtu-ignore` advice, VXLAN/MPLS overhead figures, ping DF verification, and the second source (a 404).
Method: documentation only; no commands were run.
