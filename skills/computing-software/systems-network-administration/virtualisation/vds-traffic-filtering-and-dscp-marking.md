---
id: computing-software.systems-network-administration.virtualisation.vds-traffic-filtering-and-dscp-marking
name: vds-traffic-filtering-and-dscp-marking
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [traffic-filtering-marking, dscp-marking, cos-marking, vds, qos, vmware, vsphere]
level: advanced
status: draft
description: "Use vDS traffic filtering and marking rules to drop, allow or tag VM and vmkernel traffic with DSCP and CoS values so physical QoS policies apply."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vDS traffic filtering and DSCP/CoS marking

**Goal:** mark (or drop) traffic at the virtual port so the physical network can prioritise it, without relying on guests.

## Where rules live
Distributed port group (or an uplink port group) -> Configure -> Traffic filtering and marking -> Enable, then add rules. Rules are evaluated in order; first match wins.

## Rule anatomy
- **Action**: Allow, Drop, or Tag.
- **Tag**: CoS value (802.1p, 0-7) and/or DSCP value (0-63). Common: voice EF (46), video AF41 (34), vMotion CS1 (8, scavenger), storage AF31 (26).
- **Direction**: ingress (into the switch from the VM), egress, or both.
- **Qualifiers**: system traffic type (vMotion, vSAN, NFS, management, iSCSI, VM), MAC (src/dst/VLAN/EtherType), IP (protocol, ports, addresses).

## Example: mark a VoIP port group
Rule "voice-ef": Tag, DSCP 46, CoS 5, ingress, qualifier IP protocol UDP dst ports 16384-32767.

## Example: mark vMotion low priority
On the uplink port group: Tag DSCP 8, qualifier system traffic = vMotion, egress.

## Gotchas
- DSCP set here overwrites the guest marking; to trust the guest, do not add a Tag rule for that traffic.
- CoS only travels on tagged frames (VLAN trunk); on access ports it is lost.
- Drop rules are a coarse firewall without logging; use NSX or the guest firewall for real policy.
- vDS 5.5+ is required; standard switches have no marking.

## Verify
`pktcap-uw --uplink vmnic0 --dir 1 -o - | tcpdump-uw -r - -vv` on the host shows the expected `tos 0xb8` (DSCP 46) on egress frames; switch QoS counters increment in the right queue.
