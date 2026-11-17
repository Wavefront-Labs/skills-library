---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-group-tables
name: ofctl-group-tables
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, add-group, select-group, group, buckets, fast-failover, ovs-ofctl, dp-hash]
level: advanced
status: docs-checked
description: "Manage OpenFlow groups with ovs-ofctl add-group, dump-groups and del-groups: group types all/select/indirect/ff, bucket parameters, selection methods and the group action."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl group tables
The group commands work only with switches that support OpenFlow 1.1 or later (or the OVS group extensions to OpenFlow 1.0); for 1.1 or later enable the version with `-O`.

Commands (ovs-ofctl(8)):
```
ovs-ofctl [--bundle] add-group switch group
ovs-ofctl [--bundle] add-groups switch file
ovs-ofctl [--bundle] [--may-create] mod-group switch group
ovs-ofctl [--bundle] del-groups switch [group]
ovs-ofctl [--bundle] insert-buckets switch group
ovs-ofctl [--bundle] remove-buckets switch group
ovs-ofctl dump-groups switch [group]
ovs-ofctl dump-group-features switch
ovs-ofctl dump-group-stats switch [group]
```
Lines passed to `add-group`/`add-groups` may begin with `add`, `modify`, `add_or_mod`, `delete`, `insert_bucket` or `remove_bucket`; bare means add. `del-groups switch` with no group deletes all groups. `dump-groups` with no group, or ALL, prints all; dumping one group needs OpenFlow 1.5 or later (earlier versions always dump all).

Group spec fields (only the last instance of a repeated field is honoured):
- `group_id=id` required; `all` may be used in del-groups and dump-groups.
- `type=`: `all` (execute all buckets), `select` (one bucket, balanced by weight), `indirect` (the one bucket), `ff` or `fast_failover` (first live bucket whose port or group is live). Required by add-group, add-groups and mod-group; prohibited for other commands.
- `command_bucket_id=` (integer, `all`, `first`, `last`) required by insert-buckets and remove-buckets, prohibited otherwise.
- `selection_method=` for select groups: `dp_hash` or `hash`. With none, OVS up to 2.9 uses `hash`; from 2.10 it defaults to `dp_hash` with a symmetric L3/L4 hash, falling back to `hash` when the weighted buckets cannot be mapped accurately (limit 64 buckets in 2.10, 256 from 2.17). `selection_method_param=` is a 64-bit integer (default 0). `fields=` is for `hash` only; `dp_hash` does not support it. These use a Netronome extension that needs OVS 2.4+ and OpenFlow 1.5+.
- `bucket=` needs at least one for add-group/mod-group, must appear after all other fields, and repeats; bucket order is the order in the group. Bucket parameters are `bucket_id` (OVS 2.4+, OpenFlow 1.5; values above 0xffffff00 reserved; auto-allocated if absent), `actions=` (any unknown parameter is read as an action), `weight`, `watch_port`, `watch_group`. `watch_port` or `watch_group` is required for `ff`; they may also be used for `select`. An `indirect` group takes only one bucket.

Example shape: `ovs-ofctl -O OpenFlow13 add-group br0 group_id=1,type=select,bucket=weight=1,output:1,bucket=weight=1,output:2` (bucket parameters first, then actions, per the Group Syntax text).

Use in a flow with the `group:group` action: group is 0 to 4294967040 (0xffffff00); the group must exist or OVS refuses to add the flow, and deleting a group also deletes the flows that output to it. Example: `ovs-ofctl -O OpenFlow13 add-flow br0 in_port=1,actions=group:1`.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (Group Table Commands, Group Syntax) and ovs-actions(7) (group action). Removed the Verify line; added the selection-method defaults, command semantics and flow-deletion note. The bucket example was composed from the page's bucket syntax and not taken verbatim.
Method: documentation only; no commands were run.
