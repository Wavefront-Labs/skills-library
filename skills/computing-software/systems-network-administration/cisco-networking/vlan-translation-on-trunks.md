---
id: computing-software.systems-network-administration.cisco-networking.vlan-translation-on-trunks
name: vlan-translation-on-trunks
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9000, vlan-translation, vlan-mapping, switchport-vlan-mapping, trunking, selective-qinq, nexus]
level: practitioner
status: draft
description: "Map customer or legacy VLAN IDs to local VLANs on a trunk with switchport vlan mapping (one-to-one and selective QinQ) on Catalyst 9000 and Nexus."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_vlan_mapping.html
  - https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/93x/layer2/configuration/guide/b-cisco-nexus-9000-nx-os-layer-2-switching-configuration-guide-93x/b-cisco-nexus-9000-nx-os-layer-2-switching-configuration-guide-93x_chapter_01001.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN mapping (translation) on trunks

## When
- Merging two networks whose VLAN IDs clash (both use VLAN 10 for different things).
- Handing off to a provider or tenant who uses different IDs.
- Migrating VLAN numbering one side at a time.

## One-to-one mapping (Catalyst 9000)
```
interface Gi1/0/48
 switchport mode trunk
 switchport vlan mapping 10 210       ! customer VLAN 10 arrives, switched locally as 210
 switchport vlan mapping 20 220
 switchport trunk allowed vlan 210,220   ! allow the translated (local) IDs
show interfaces Gi1/0/48 vlan mapping
```
Traffic leaving the port in VLAN 210 is rewritten back to 10.

## Selective QinQ
```
interface Gi1/0/48
 switchport vlan mapping 100-110 dot1q-tunnel 500   ! push outer tag 500 for C-VLANs 100-110
```

## Nexus 9000
```
interface Ethernet1/10
 switchport mode trunk
 switchport vlan mapping enable
 switchport vlan mapping 10 210
 switchport trunk allowed vlan 210
show interface Ethernet1/10 vlan mapping
```

## Gotchas
- Allowed VLAN list refers to the **local** (translated) ID on Catalyst.
- Do not also carry the original ID natively on the same port; mapping and a real VLAN of the same number clash.
- STP: translated VLAN runs PVST instance for the local ID; BPDUs from the far side arrive with
  the remote ID and can cause inconsistent-port states if PVST meets PVST across a mapping. Run
  BPDU filtering or a routed hand-off where possible.
- Mapping support and scale are platform/ASIC specific; check the release notes.

## Verify
- [ ] `show interfaces <port> vlan mapping` lists each pair.
- [ ] Host in customer VLAN 10 reaches gateway in local VLAN 210; captures show tag 10 on the wire side.
