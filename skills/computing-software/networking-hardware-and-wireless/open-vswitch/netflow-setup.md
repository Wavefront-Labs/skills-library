---
id: computing-software.networking-hardware-and-wireless.open-vswitch.netflow-setup
name: netflow-setup
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, netflow, active-timeout, engine-id, collector, flow-export]
level: practitioner
status: docs-checked
description: "Export NetFlow records from an Open vSwitch bridge: create a NetFlow record with targets and active-timeout, attach to the bridge, engine ids, and the port-count limit."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# netflow setup
Cookbook form (UDP port 5566 on 192.168.0.34, active timeout 30 seconds):
`ovs-vsctl -- set Bridge br0 netflow=@nf -- --id=@nf create NetFlow targets=\"192.168.0.34:5566\" active-timeout=30`

Update it later with `ovs-vsctl set NetFlow br0 active_timeout=60`.

NetFlow columns:
- `targets`: one or more `ip:port` strings; the IP must be numeric.
- `active_timeout`: seconds, at least -1. 0 uses the default of 600; -1 disables active timeouts.
- `engine_type` and `engine_id`: 0 to 255; default to the datapath index.
- `add_id_to_interface`: boolean; when true the 7 most significant bits of the ingress and egress interface fields are replaced by the least significant 7 bits of the engine id, and at most 508 ports are supported.

Remove: `ovs-vsctl clear Bridge br0 netflow` (also destroys the now unreferenced NetFlow record).

The passive timeout for inactive flows is not configurable.

Verify: `ovs-vsctl list netflow` and a packet capture on the collector port.

Gotcha: the ovs-vsctl example quotes the target as `\"ip:port\"`; copy that form, and give the IP numerically, not as a DNS name.

## Checked

2026-11-09. Confirmed against the NetFlow section of ovs-vsctl(8) and the NetFlow table of ovs-vswitchd.conf.db(5): cookbook create, update and clear commands, targets format, active_timeout semantics, engine_type and engine_id ranges and defaults, add_id_to_interface and the 508 port limit, list command. Removed: the claim that unquoted colons are rejected (not stated).
Method: documentation only; no commands were run.
