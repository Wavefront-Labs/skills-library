---
id: computing-software.systems-network-administration.cisco-networking.vlan-and-trunking-configuration
name: vlan-and-trunking-configuration
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, catalyst, vlan, trunk, 802-1q, dtp, dynamic-auto, dynamic-desirable, vtp, vtpv3, vtp-primary, extended-vlan, etherchannel, port-channel, lacp, pagp, channel-group, load-balance, private-vlan, pvlan, isolated-vlan, community-vlan, promiscuous-port, vlan-hopping, double-tagging, switch-spoofing, voice-vlan, lldp-med, trunk-troubleshooting, show-etherchannel-summary]
level: advanced
status: draft
description: "Cisco trunking beyond the basics: DTP outcome matrix, VTPv3 primary server, LACP EtherChannel trunks, private VLANs, VLAN-hopping hardening and a trunk fault-finding table."
sources:
  - https://www.cisco.com/c/en/us/support/switches/catalyst-9300-series-switches/products-installation-and-configuration-guides-list.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/vtp/10558-21.html
  - https://www.cisco.com/c/en/us/support/docs/lan-switching/etherchannel/12023-4.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VLAN and trunking configuration — the parts that cause outages after day one

**Goal:** run trunks that negotiate predictably, bundle cleanly, propagate VLANs safely and
resist VLAN-hopping. Basic VLAN creation, access ports, native/allowed lists and SVIs are
in `computing-software.systems-network-administration.cisco-networking.vlans-trunks-and-inter-vlan-routing`;
this skill assumes that baseline.

## 1. DTP: know the outcome before you plug in
| Side A \ Side B | access | trunk | dynamic desirable | dynamic auto |
|---|---|---|---|---|
| **access** | access | mismatch | access | access |
| **trunk** | mismatch | trunk | trunk | trunk |
| **dynamic desirable** | access | trunk | trunk | trunk |
| **dynamic auto** | access | trunk | trunk | **access** |

- Two switches left at `dynamic auto` (a common default on Catalyst access switches)
  never form a trunk: the uplink silently becomes an access port in VLAN 1.
- `switchport nonegotiate` stops DTP frames, so the far side must be hard-set to
  `trunk` too; it will not negotiate anything.
- Check what actually happened: `show dtp interface Gi1/0/48` and
  `show interfaces Gi1/0/48 switchport` (Administrative vs Operational Mode).

## 2. VTP done safely
If you want VLANs propagated, use **VTPv3**, not v1/v2:
```
vtp domain CAMPUS
vtp version 3
vtp password <VTP_SECRET>
vtp mode server
! then, in privileged EXEC (not config mode):
vtp primary vlan
```
Only the switch that took `vtp primary` can change the VLAN database; other servers are
secondary and cannot overwrite it by having a higher revision. v3 also carries extended
VLANs (1006–4094). With v1/v2 you need `vtp mode transparent` to create extended VLANs.
Before inserting any used switch into a v1/v2 domain, set it to transparent (resets the
revision to 0) or you risk the revision-number wipe.

## 3. EtherChannel trunks (LACP)
```
interface range Te1/1/1 - 2
 channel-group 10 mode active        ! LACP; never "on" toward a device you don't control
interface Port-channel10
 switchport mode trunk
 switchport nonegotiate
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,99
port-channel load-balance src-dst-ip  ! global; options and default vary by platform
```
- Members must match speed, duplex, switchport mode, native and allowed VLANs. Make
  trunk changes on the **Port-channel**, which pushes them to members; editing one member
  suspends it.
- `mode on` forms the bundle without negotiation. If the other end is not bundled you get
  a loop or MAC flapping; LACP `active`/`passive` (or PAgP `desirable` on Cisco-only
  links) fails safe.
- `show etherchannel summary`: `P` bundled, `s` suspended, `I` stand-alone, `D` down. `SU`
  on the Port-channel means layer 2 and up.
- Load balance hashes per flow, so one large flow never exceeds one member's speed.

## 4. Private VLANs (isolating hosts in one subnet)
Useful for DMZs, hotel/guest wired ports, or server out-of-band networks. Requires VTP
transparent or v3.
```
vlan 101
 private-vlan isolated
vlan 102
 private-vlan community
vlan 100
 private-vlan primary
 private-vlan association 101,102
interface Gi1/0/5
 switchport mode private-vlan host
 switchport private-vlan host-association 100 101
interface Gi1/0/48                     ! router/firewall
 switchport mode private-vlan promiscuous
 switchport private-vlan mapping 100 101,102
```
Isolated ports reach only promiscuous ports; community ports reach each other and the
promiscuous port. With an SVI as gateway, add `private-vlan mapping 101,102` under
`interface Vlan100`. Support differs by platform and licence (unconfirmed on every
Catalyst model; check the configuration guide).

## 5. Harden against VLAN hopping
- **Switch spoofing** (host negotiating a trunk): `switchport mode access` +
  `nonegotiate` on every edge port.
- **Double tagging** (outer tag = native VLAN stripped, inner tag delivered): native VLAN
  on trunks is an unused VLAN that no access port uses, or `vlan dot1q tag native`.
- Do not use VLAN 1 for users or management; remove it from trunks where the platform
  allows (`switchport trunk allowed vlan remove 1`). Control protocols (CDP, VTP, DTP,
  PAgP) still run on VLAN 1.
- Voice VLAN: phones learn it via CDP or LLDP-MED; enable `lldp run` for non-Cisco phones.

## 6. Trunk fault-finding
| Symptom | Likely cause | Check |
|---|---|---|
| VLAN in "allowed" but not "allowed and active" | VLAN not created on this switch | `show vlan id N` |
| Allowed and active, not "forwarding and not pruned" | STP blocking or VTP pruning | `show spanning-tree vlan N` |
| `%CDP-4-NATIVE_VLAN_MISMATCH` | native VLAN differs per side | both ends `show interfaces trunk` |
| Port-channel member `s` | member config differs | `show run int` on each member |
| Uplink works only for one VLAN | DTP fell back to access | `show interfaces X switchport` |

## Verify
- [ ] Every switch-to-switch link has a predictable mode (both sides `trunk` + `nonegotiate`, or LACP bundle).
- [ ] VTP is v3 with one primary, or transparent/off everywhere; `show vtp status` agrees.
- [ ] `show etherchannel summary` shows all members `P`, no `s`/`I`.
- [ ] No access port is in the native VLAN of any trunk; VLAN 1 carries no user traffic.
- [ ] Private-VLAN hosts cannot ping each other but reach the gateway (test from two isolated ports).
