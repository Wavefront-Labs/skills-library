---
id: computing-software.networking-hardware-and-wireless.open-vswitch.stp-and-rstp
name: stp-and-rstp
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, stp, rstp, spanning-tree, stp-priority, loops, forward-bpdu]
level: practitioner
status: docs-checked
description: "Enable STP or RSTP on an Open vSwitch bridge to prevent loops, tune priority and timers, set per-port options, inspect with stp/show, and handle BPDU forwarding."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
  - https://docs.openvswitch.org/en/latest/faq/issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# stp and rstp
For a redundant or complex topology where you want to prevent loops, the FAQ enables STP like this (the order matters so there is never even a transient loop):
```
ovs-vsctl add-br br0
ovs-vsctl set bridge br0 stp_enable=true
ovs-vsctl add-port br0 eth0
ovs-vsctl add-port br0 eth1
```
The FAQ warns that the OVS STP implementation is not well tested.

Both are disabled by default. STP and RSTP are mutually exclusive; if both are enabled, RSTP is used (`rstp_enable=true`). Bond, internal and mirror ports are not supported and do not participate in the spanning tree.

Bridge `other_config` (STP, strings):
- `stp-priority` 0 to 65535, default 0x8000; lowest bridge-id becomes root
- `stp-hello-time` 1 to 10 s, default 2
- `stp-max-age` 6 to 40 s, default 20
- `stp-forward-delay` 4 to 30 s, default 15
- `stp-system-id` xx:xx:xx:xx:xx:xx, default the bridge MAC

Bridge `other_config` (RSTP): `rstp-priority` 0 to 61440, default 0x8000 (32768), should be a multiple of 4096 (otherwise rounded down to the nearest one); `rstp-address`; `rstp-ageing-time` 10 to 1000000, default 300 s; `rstp-force-protocol-version` 0 (STP compatibility) or 2 (default); `rstp-max-age` 6 to 40, default 20; `rstp-forward-delay` 4 to 30, default 15; `rstp-transmit-hold-count` 1 to 10, default 6.

Port `other_config` (STP): `stp-enable` (on by default for all ports once the bridge has STP, set false to disable on a port), `stp-port-priority` 0 to 255 (default 0x80), `stp-path-cost` 0 to 65535 (default based on link speed), `stp-port-num` 1 to 255 (if you set one on a bridge you must set them all). RSTP has parallel keys: `rstp-enable`, `rstp-port-priority`, `rstp-port-num`, `rstp-path-cost`, `rstp-port-admin-edge`, `rstp-port-auto-edge`, `rstp-port-mcheck`.

BPDUs: Bridge `other_config:forward-bpdu` (true or false, default unset = false). When false or unset, frames with reserved Ethernet addresses are not forwarded by the NORMAL action. Set it true if the bridge connects different Ethernet networks and does not participate in STP. If STP is enabled on the bridge, it processes all received STP packets and never forwards them, even if STP is disabled on an individual port.

Inspect with ovs-appctl against ovs-vswitchd: `stp/show [bridge]`, `rstp/show [bridge]` (all STP/RSTP bridges if none is named). `stp/tcn [bridge]` and `rstp/tcn [bridge]` force a topology change event, which may send Topology Change Notifications to peers and flush the MAC table.

## Checked
2026-11-04. Confirmed against ovs-vswitchd.conf.db(5) (Bridge STP and RSTP configuration, `forward-bpdu`, Port STP configuration), ovs-vswitchd(8) (stp/show, stp/tcn, rstp/show, rstp/tcn) and the FAQ issues page (STP example). Removed the unsourced Verify line about a blocking role and the Gotcha about `bond_updelay` and forwarding delay.
Method: documentation only; no commands were run.
