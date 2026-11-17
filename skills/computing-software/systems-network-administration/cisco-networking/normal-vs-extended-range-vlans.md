---
id: computing-software.systems-network-administration.cisco-networking.normal-vs-extended-range-vlans
name: normal-vs-extended-range-vlans
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst-9300, vlan, extended-range-vlan, vtp, vlan-dat]
level: practitioner
status: docs-checked
description: "Normal-range (1-1005) vs extended-range (1006-4094) VLANs on Catalyst 9300: where each is stored, VTP version and mode requirements, pruning and edit limits, vlan.dat on reset."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/vlan/b_179_vlan_9300_cg/configuring_vlans.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Normal vs extended-range VLANs

Scope: Catalyst 9300 IOS XE 17.9 VLAN configuration guide (Configuring VLANs). Up to 4094 VLANs can be configured,
but not all can be active at once.

## Ranges
| Range | Notes (from the guide) |
|---|---|
| 1 | Default VLAN, created at initialisation, cannot be deleted |
| 2-1001 | Normal range; configured in the VLAN database (`vlan.dat` in flash) in VTP server or transparent mode |
| 1002-1005 | Reserved for Token Ring and FDDI; created automatically and cannot be removed |
| 1006-4094 | Extended range |

Normal-range VLANs (1-1005) are always saved in the VLAN database; in VTP transparent mode they are also saved in
the running configuration. Before creating a VLAN the switch must be in VTP server or transparent mode (a server
needs a VTP domain).

## Extended-range rules
- With VTP version 1 or 2, extended-range VLANs are not stored in the VLAN database and are not recognised by VTP;
  set VTP mode transparent, and save the configuration to startup or the VLANs are lost on reset. They live in
  the running configuration.
- With VTP version 3, extended-range VLANs are recognised by VTP and stored in the VLAN database. Creating extended
  VLANs under VTP version 3 means you cannot convert back to VTP version 1 or 2.
- Extended-range VLANs cannot be in the pruning-eligible range.
- Only the MTU size, private VLAN and remote SPAN state can be changed on an extended-range VLAN; everything else
  stays at defaults.
- IDs 1006-4094 are accepted by any switchport command that takes VLAN IDs.

```
vtp mode transparent
vlan 2001
 end
copy running-config startup-config
```
The `vlan` command accepts 1 to 4094; the extended-range creation step documents the range as 1006 to 4094.

## On reset
Delete the `vlan.dat` file along with the configuration files before using `write erase`, so the switch reboots
correctly on a reset. Do not delete `vlan.dat` manually otherwise: the guide warns it can make the VLAN database
inconsistent.

## Deleting
Deleting a VLAN on a VTP server removes it from the database for the whole VTP domain; on a transparent switch only
on that device. Default VLANs (1 and 1002-1005) cannot be deleted.

## Checked
Date: 2026-11-08
Method: documentation only; no commands were run. Read the Catalyst 9300 17.9 "Configuring VLANs" chapter:
Information About VLANs, Normal-Range and Extended-Range VLAN Configuration Guidelines, How to Configure Extended-Range
VLANs and the VLAN deletion text (located by searching for range, vlan.dat and VTP terms, then reading those
paragraphs; the chapter was not read end to end). The second cited page, document 10558, was fetched but not used, and
is dropped from sources. Corrected: the old table said 2-1001 only in vlan.dat and that 0/4095 were reserved (the guide
says 1-1005 are stored in vlan.dat and IDs run 1 to 4094); VTP version 3 stores extended VLANs in the database, not
only in the config. Removed as unconfirmed: CDP/VTP/PAgP/DTP on VLAN 1, the internal VLAN allocation section
(`show vlan internal usage`, `allocation policy descending`, the Port Manager error), the "higher revision wipes
joiners" line, the claim that older private VLAN code and third-party gear lack extended-ID support, and the Nexus
reserved range.
