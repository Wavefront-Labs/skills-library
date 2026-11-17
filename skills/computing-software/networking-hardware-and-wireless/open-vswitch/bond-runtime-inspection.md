---
id: computing-software.networking-hardware-and-wireless.open-vswitch.bond-runtime-inspection
name: bond-runtime-inspection
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, bond-show, lacp-show, bond-migrate, ovs-appctl, bonding, fdb]
level: practitioner
status: docs-checked
description: "Inspect and nudge live Open vSwitch bonds with ovs-appctl: bond/list, bond/show, lacp/show, lacp/stats-show, bond/migrate, set-active-member, enable/disable-member, and fdb/show."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vswitchd.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# bond runtime inspection
Read-only:
- `ovs-appctl bond/list` lists all bonds and their members on each bridge.
- `ovs-appctl bond/show [port]` lists updelay, downdelay, time until the next rebalance, and per-member enabled/disabled state, pending delay time, whether it is the active member and its assigned hashes (all bonded ports if no port).
- `ovs-appctl bond/hash mac [vlan] [basis]` returns the hash value that would be used for that MAC.
- `ovs-appctl lacp/show [port]` lists LACP information: active or passive, aggregation key, system id and priority, and per member enabled/attached state, port id and priority, actor and partner information.
- `ovs-appctl lacp/stats-show [port]` lists LACP PDU counts (RX/TX, bad PDUs) and member state counts (state expired/defaulted, carrier changed).
- `ovs-appctl fdb/show [bridge...]` lists each learned MAC/VLAN pair, its port and entry age in seconds.

Temporary changes (rebalancing, fail-over or a carrier change can undo them):
- `ovs-appctl bond/migrate bond0 HASH eth1` assigns a MAC hash (decimal 0 to 255) to a member; SLB bonds only; a hash cannot be migrated to a disabled member.
- `ovs-appctl bond/set-active-member bond0 eth1` sets the active member, which must currently be enabled; a new one is chosen if it becomes disabled.
- `ovs-appctl bond/enable-member bond0 eth1` and `bond/disable-member bond0 eth1` skip any updelay or downdelay and persist only until the member's carrier status changes.

With `other_config:lb-output-action` set to `true` (balance-tcp only), the userspace datapath handles bond load balancing directly, and `ovs-appctl dpif-netdev/bond-show [dp]` prints the bond load-balancing information.

## Checked
2026-11-04. Confirmed against ovs-vswitchd(8) (Bond commands, `fdb/show`, `dpif-netdev/bond-show`). Removed the claim that `bond-show` prints a bucket-to-interface map, and the generic failover Verify line.
Method: documentation only; no commands were run.
