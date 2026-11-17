---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vlan-mode-values
name: vlan-mode-values
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, vlan-mode, dot1q-tunnel, native-tagged, native-untagged, trunk, access, qinq]
level: advanced
status: docs-checked
description: "Choose the Port vlan_mode in Open vSwitch (access, trunk, native-tagged, native-untagged, dot1q-tunnel), how tag and trunks interact, and the QinQ ethertype setting."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vlan mode values
Port column `vlan_mode` is an optional string, one of `access`, `dot1q-tunnel`, `native-tagged`, `native-untagged`, `trunk`:
- `access`: exactly one VLAN, given by `tag`; egress packets have no 802.1Q header; ingress packets with a nonzero VLAN ID in an 802.1Q header are dropped. Default when `vlan_mode` is empty and `tag` has a value.
- `trunk`: carries the VLANs in `trunks` (empty = all). Ingress packets are in the VLAN of their 802.1Q header, or VLAN 0 if none; ingress packets tagged with a VLAN the port does not trunk are dropped. Default otherwise.
- `native-tagged`: like trunk, except a packet without an 802.1Q header is in the native VLAN given by `tag`.
- `native-untagged`: like native-tagged, except a packet egressing in the native VLAN has no 802.1Q header.
- `dot1q-tunnel`: like an access port, carrying the service VLAN given by `tag`, but a packet with an 802.1Q header is treated as double-tagged (the header is the inner customer VLAN). `cvlans` limits the customer VLANs; empty means all.

Related columns:
- `tag`: optional integer 0 to 4095; must be empty for a trunk port.
- `trunks`: up to 4096 integers, 0 to 4095; must be empty for an access port; a native-tagged or native-untagged port always trunks its native VLAN.
- `other_config:qinq-ethtype`: `802.1ad` (TPID 0x88a8, the default) or `802.1q` (TPID 0x8100); sets the TPID of the service tag for a dot1q-tunnel port.

Examples:
- `ovs-vsctl set port eth0 vlan_mode=native-untagged tag=1 trunks=10,20`
- `ovs-vsctl set port tap0 vlan_mode=dot1q-tunnel tag=100`

The VLAN configuration affects Open vSwitch only for normal switching; it does not affect flows set up by an OpenFlow controller outside the `normal` action (see actions-header-rewrite).

## Checked
2026-11-04. Confirmed against ovs-vswitchd.conf.db(5) Port table (VLAN configuration text, `vlan_mode`, `tag`, `trunks`, `cvlans`, `qinq-ethtype`). Removed the invented `ovs-vsctl get port ...` Verify line.
Method: documentation only; no commands were run.
