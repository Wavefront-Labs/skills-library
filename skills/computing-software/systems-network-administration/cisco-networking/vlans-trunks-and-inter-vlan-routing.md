---
id: computing-software.systems-network-administration.cisco-networking.vlans-trunks-and-inter-vlan-routing
name: vlans-trunks-and-inter-vlan-routing
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst, vlan, 802-1q, dot1q, trunk, access-port, native-vlan, allowed-vlans, switchport, dtp, nonegotiate, inter-vlan-routing, router-on-a-stick, subinterface, svi, layer-3-switch, ip-routing, spanning-tree, stp, rapid-pvst, portfast, bpduguard, show-vlan, show-interfaces-trunk, write-memory, juniper, aruba]
level: practitioner
status: draft
description: "Cisco IOS VLANs: access and trunk ports, native and allowed VLANs, router-on-a-stick vs SVIs, PortFast/BPDU Guard, verification show commands and saving config."
sources:
  - https://www.cisco.com/c/en/us/support/switches/catalyst-9300-series-switches/products-installation-and-configuration-guides-list.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLANs, trunks and inter-VLAN routing on Cisco IOS — explicit everything

**Goal:** segment a switched network into VLANs, carry them safely between switches,
route between them, and prove it with show commands before saving.

Example plan (documentation ranges): VLAN 10 Users `198.51.100.0/25`, VLAN 20 Voice
`198.51.100.128/26`, VLAN 99 Management `192.0.2.0/27`, VLAN 999 unused/native.

## 1. Create VLANs
```
conf t
 vlan 10
  name USERS
 vlan 20
  name VOICE
 vlan 99
  name MGMT
 vlan 999
  name NATIVE-UNUSED
end
```
VTP can propagate (or wipe) VLAN databases across switches. Unless you deliberately run
VTPv3, set `vtp mode transparent` (or `off` where supported) so a stray switch with a
higher revision cannot delete your VLANs.

## 2. Access ports
```
interface range GigabitEthernet1/0/1 - 24
 description USER-DESK
 switchport mode access
 switchport access vlan 10
 switchport voice vlan 20
 switchport nonegotiate
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
```
- `switchport mode access` + `nonegotiate` turns off DTP so a host cannot negotiate a trunk.
- **PortFast** skips listening/learning (~30 s with classic STP) so DHCP works at boot.
  **BPDU Guard** err-disables the port if a switch is plugged in. Global alternative:
  `spanning-tree portfast default` and `spanning-tree portfast bpduguard default` (apply
  to access ports only). Recover with `shutdown`/`no shutdown` or
  `errdisable recovery cause bpduguard` + `errdisable recovery interval 300`.
- Shut unused ports and put them in an unused VLAN.

## 3. Trunks
```
interface TenGigabitEthernet1/1/1
 description UPLINK-to-DIST1
 switchport trunk encapsulation dot1q   ! only on platforms that also support ISL
 switchport mode trunk
 switchport nonegotiate
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,99
```
- **Native VLAN** carries untagged frames. Set it to an unused VLAN, identical on both
  ends; a mismatch leaks traffic between VLANs and CDP logs `%CDP-4-NATIVE_VLAN_MISMATCH`.
  `vlan dot1q tag native` (global) tags it too, where supported.
- **Allowed list:** prune to what is needed. To add later, use
  `switchport trunk allowed vlan add 30`. Typing `allowed vlan 30` without `add`
  **replaces** the list and drops every other VLAN on that uplink — a classic outage.

## 4. Inter-VLAN routing
**Layer-3 switch with SVIs** (preferred: wire-speed, no hairpin):
```
ip routing
interface Vlan10
 ip address 198.51.100.1 255.255.255.128
 ip helper-address 192.0.2.10        ! DHCP server in another VLAN
 no shutdown
interface Vlan20
 ip address 198.51.100.129 255.255.255.192
 no shutdown
```
An SVI is up/up only if the VLAN exists and at least one port in it (access or trunk
forwarding that VLAN) is up.

**Router-on-a-stick** (small sites, router or firewall with one trunk link):
```
interface GigabitEthernet0/0
 no shutdown
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 198.51.100.1 255.255.255.128
interface GigabitEthernet0/0.999
 encapsulation dot1Q 999 native
```
All inter-VLAN traffic crosses that one link twice, so bandwidth caps out at the link
speed. Filter between VLANs with ACLs on SVIs/subinterfaces or route through a firewall.

## 5. Verify, then save
```
show vlan brief                      ! VLANs and access-port membership
show interfaces trunk                ! mode, native VLAN, allowed and forwarding VLANs
show interfaces Gi1/0/5 switchport   ! admin vs operational mode
show spanning-tree vlan 10           ! root bridge, port roles
show ip interface brief              ! SVI/subinterface status
show interfaces status err-disabled
show mac address-table vlan 10
```
In `show interfaces trunk`, a VLAN missing from "allowed and active" or "forwarding
state and not pruned" points to a missing VLAN or an STP block. Set the root bridge
deliberately (`spanning-tree vlan 10,20,99 root primary` on the core/distribution) rather
than letting the oldest switch win; Rapid PVST+ (`spanning-tree mode rapid-pvst`) is the
usual default choice.

Save: `copy running-config startup-config` (or `write memory`). For risky remote changes,
schedule a safety net first: `reload in 10`, make the change, then `reload cancel` once
you are still connected.

## Verify
- [ ] Every access port is `mode access`, `nonegotiate`, PortFast + BPDU Guard.
- [ ] Trunks have an explicit allowed list and the same unused native VLAN on both ends.
- [ ] `show interfaces trunk` lists every needed VLAN as forwarding on each uplink.
- [ ] Hosts in different VLANs can ping each other's gateways and each other (or are blocked by ACL as intended).
- [ ] STP root is the intended switch.
- [ ] Config saved to startup; any `reload in` timer cancelled.
