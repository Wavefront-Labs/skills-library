---
id: computing-software.networking-hardware-and-wireless.open-vswitch.vlan-access-and-trunk-ports
name: vlan-access-and-trunk-ports
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, vlan-tag, trunks, access-port, vlan, internal-port]
level: intro
status: docs-checked
description: "Isolate VM traffic with VLANs in Open vSwitch: access ports with tag=, default trunk ports, trunks lists, and an internal port for a host VLAN interface."
sources:
  - https://docs.openvswitch.org/en/latest/howto/vlan/
  - https://docs.openvswitch.org/en/latest/faq/configuration/
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vlan access and trunk ports
Access ports (traffic from the VM is untagged and considered part of the VLAN):
- `ovs-vsctl add-port br0 tap0 tag=100`
- `ovs-vsctl add-port br0 tap1 tag=200`
- Convert an existing port: `ovs-vsctl set port tap0 tag=9`

Trunk (the default): by default all OVS ports are VLAN trunks, so `ovs-vsctl add-port br0 eth0` passes all VLANs.

Limit a trunk with the Port `trunks` column: up to 4096 integers (0 to 4095); if empty, the port trunks all VLANs.
`ovs-vsctl set port eth0 trunks=100,200`

Host-side VLAN interface on the bridge itself (an example in ovs-vsctl(8)):
`ovs-vsctl add-port br0 vlan10 tag=10 -- set Interface vlan10 type=internal`
This adds an internal port as an access port for VLAN 10, to which an IP address can then be assigned.

Expected result in the how-to: VMs on the same VLAN can ping each other across hosts; VMs on different VLANs cannot unless a router forwards between them. When eth0 is added to a bridge, IP addresses assigned to it stop working, so move them to another interface first (the how-to uses a separate management NIC).

Notes:
- `tag` and `trunks` are Port columns, so `add-port ... tag=` sets the same column as `set port ... tag=`.
- If `vlan_mode` is empty and `tag` has a value the port is an access port (`trunks` should be empty); otherwise it is a trunk (see vlan-mode-values).
- VLAN configuration affects only "normal switching" and the OpenFlow `normal` action, not flows set up by an OpenFlow controller.
- Bridge column `flood_vlans` lists VLANs on which MAC learning is disabled so packets are flooded; ordinarily used for RSPAN mirror VLANs.

## Checked
2026-11-04. Confirmed against the OVS VLAN how-to, ovs-vsctl(8) (add-port, Examples) and ovs-vswitchd.conf.db(5) (Port `tag`, `trunks`, `vlan_mode`; Bridge `flood_vlans`). Removed the `list port` inspection hint and tightened the wording of the notes to match the pages.
Method: documentation only; no commands were run.
