---
id: computing-software.systems-network-administration.cisco-networking.qinq-dot1q-tunnelling
name: qinq-dot1q-tunnelling
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, catalyst, qinq, dot1q-tunnel, 802-1ad, metro-ethernet, l2protocol-tunnel]
level: practitioner
status: draft
description: "Carry customer VLANs across a provider VLAN with 802.1Q tunnelling: dot1q-tunnel ports, MTU for the extra tag, L2 protocol tunnelling of CDP/STP, and native VLAN traps."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9500/software/release/17-9/configuration_guide/lyr2/b_179_lyr2_9500_cg/configuring_ieee_802_1q_tunneling.html
  - https://standards.ieee.org/ieee/802.1Q/10323/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 802.1Q tunnelling (QinQ)

A provider (or a campus core) adds an outer "S-tag" VLAN to everything a customer port sends,
carrying all the customer's VLANs transparently through one service VLAN.

## Configure the tunnel port
```
vlan 500
 name CUST-A-SVC
interface Gi1/0/1
 description CUST-A handoff
 switchport access vlan 500
 switchport mode dot1q-tunnel
 l2protocol-tunnel cdp
 l2protocol-tunnel stp
 l2protocol-tunnel lldp
 no cdp enable
```
Core trunks just carry VLAN 500 as a normal trunked VLAN.

## MTU
Every customer frame grows by 4 bytes (or 8 if the customer sends tagged frames into an already
tagged path). Raise MTU on every core link:
```
system mtu 1504          ! minimum; many use 9198 jumbo end to end
show system mtu
```
Symptom of missing MTU: small pings work, full-size packets and TCP bulk transfers hang.

## Layer 2 protocol tunnelling
Without `l2protocol-tunnel`, the provider switch consumes customer BPDUs/CDP. With it, they are
rewritten to a Cisco multicast MAC, carried through, and restored at the far tunnel port so the
customer's STP sees one big segment.
```
show l2protocol-tunnel summary
l2protocol-tunnel shutdown-threshold stp 1000      ! protect the core from a customer BPDU storm
```

## Gotchas
- Native VLAN on core trunks: if the S-VLAN equals the native VLAN of a core trunk it leaves
  untagged and the far side mis-classifies. Use `vlan dot1q tag native` on core switches.
- Customer's native-VLAN frames arrive untagged and get only the outer tag; on egress they leave
  untagged. Fine, but both ends must agree.
- One customer's broadcast storm floods the whole S-VLAN; apply storm-control on tunnel ports.
- Ethertype: Cisco uses 0x8100 for both tags by default; some carrier gear expects 0x88A8
  (802.1ad). Check interop.

## Verify
- [ ] `show dot1q-tunnel` lists the tunnel ports.
- [ ] Customer VLANs 10/20/30 pass end to end and customer CDP sees the far-side customer switch.
- [ ] `ping df-bit size 1500` across the tunnel succeeds.
