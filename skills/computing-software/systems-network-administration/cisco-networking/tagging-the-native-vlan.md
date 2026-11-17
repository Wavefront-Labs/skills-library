---
id: computing-software.systems-network-administration.cisco-networking.tagging-the-native-vlan
name: tagging-the-native-vlan
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, trunking, tag-native-vlan, native-vlan, vlan-hopping, double-tagging, 8021q, vlan-dot1q-tag-native]
level: practitioner
status: draft
description: "Stop double-tagging VLAN hopping by tagging the native VLAN on 802.1Q trunks, and handle the interop and control-protocol effects of doing so."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_vlan_trunks.html
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/10582-63.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tagging the native VLAN on 802.1Q trunks

## Why
Frames in the native VLAN cross a trunk untagged. An attacker on an access port in the native
VLAN can send a double-tagged frame: the first switch strips the outer (native) tag and forwards
the inner tag across the trunk, landing the frame in another VLAN (one-way VLAN hopping).
Tagging the native VLAN removes the untagged path.

## Configure
```
conf t
 vlan dot1q tag native              ! global on Catalyst: all trunks tag the native VLAN
show vlan dot1q tag native
```
Per-trunk alternatives:
```
interface Te1/1/1
 switchport trunk native vlan 998    ! unused VLAN, no access ports
 switchport trunk allowed vlan 10,20,100   ! and do not allow 998 at all
```
Making the native VLAN an unused one that is not in the allowed list is the common, interop-safe defence.

## Effects to plan for
- Both ends must agree. A tagged-native switch drops untagged ingress frames on trunks (except
  control protocols), so a neighbour sending untagged native traffic loses it.
- Control-plane frames (CDP, LLDP, PAgP/LACP, DTP, VTP, STP BPDUs on VLAN 1) still go untagged.
- Devices that need untagged traffic on a trunk (some APs in local mode for management, IP
  phones, PXE on hypervisor uplinks) break; give them a tagged management VLAN instead.
- QinQ tunnel ports: Cisco requires `vlan dot1q tag native` to avoid native-VLAN leaks between customers.

## Verify
- [ ] `show interfaces trunk` native VLAN identical both ends; `%CDP-4-NATIVE_VLAN_MISMATCH` absent.
- [ ] No access port is in the native VLAN (`show vlan id 998` has no ports).
