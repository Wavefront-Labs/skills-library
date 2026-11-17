---
id: computing-software.networking-hardware-and-wireless.open-vswitch.multicast-snooping
name: multicast-snooping
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, multicast-snooping, mcast-snooping, igmp, mdb, multicast]
level: practitioner
status: docs-checked
description: "Enable multicast snooping on an Open vSwitch bridge, tune aging time and table size, control unregistered multicast flooding, inspect the group table."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.conf.db.5.txt
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# multicast snooping
Enable per bridge (disabled by default):
`ovs-vsctl set bridge br0 mcast_snooping_enable=true`

Bridge `other_config` (string integers):
- `mcast-snooping-aging-time`: at least 1, default 300 s, forced into 15 to 3600.
- `mcast-snooping-table-size`: at least 1, default 2048, forced into 10 to 1,000,000.
- `mcast-snooping-disable-flood-unregistered`: `false` sends unregistered multicast to all ports; `true` sends it only to multicast-router ports.

Example: `ovs-vsctl set bridge br0 other_config:mcast-snooping-aging-time=600`

Inspect and reset:
- `ovs-appctl mdb/show br0` lists multicast group/VLAN pairs with port and age.
- `ovs-appctl mdb/flush [br0]` flushes the snooping table.

Gotcha: the documented bridge key is `mcast-snooping-disable-flood-unregistered`. Per-port `other_config:mcast-snooping-flood` (all multicast except Reports) and `mcast-snooping-flood-reports` (Reports) force unconditional flooding to that port.

## Checked
2026-11-09. Partial read (Bridge and Port tables) of ovs-vswitchd.conf.db(5): mcast_snooping_enable (disabled), the three bridge other_config keys with defaults and ranges, port flood keys. Read mdb/show and mdb/flush in ovs-vswitchd(8). Removed: the verify step (not in the sources).
Method: documentation only; no commands were run.
