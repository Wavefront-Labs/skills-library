---
id: computing-software.networking-hardware-and-wireless.open-vswitch.fake-vlan-bridge
name: fake-vlan-bridge
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, fake-bridge, add-br-parent, vlan, br-set-external-id]
level: practitioner
status: docs-checked
description: "Create an Open vSwitch fake bridge bound to one VLAN of a real parent bridge with add-br bridge parent vlan, and know its limits and external-id handling."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-vsctl.8.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fake vlan bridge
A fake bridge simulates, for software designed for the Linux bridge, a separate bridge for one 802.1Q VLAN; the actual implementation uses only the single parent bridge, with ports on the fake bridge assigned its implicit VLAN. A fake bridge for VLAN 0 receives packets that have no 802.1Q tag or a tag with VLAN 0.

Syntax: `ovs-vsctl [--may-exist] add-br bridge parent vlan`
- `vlan` is an integer between 0 and 4095.
- `parent` must already exist and must not itself be a fake bridge.
- The parent must not already have a fake bridge for that VLAN.
- Without `--may-exist` creating an existing bridge is an error; with it, the command does nothing if the VLAN bridge already exists under `parent`.

Example, exposing VLAN 10 of `br0` as `br0v10`:
`ovs-vsctl add-br br0v10 br0 10`

Behaviour to remember:
- Deleting a real bridge with `del-br` also deletes any fake bridges that have it as parent, including their ports.
- For a fake bridge, `br-set-external-id bridge key [value]` modifies keys prefixed `fake-bridge-` in the Port table instead of the Bridge table. Omit `value` to remove the key.
- `br-to-vlan bridge` prints the VLAN of a fake bridge (0 for a real bridge) and `br-to-parent bridge` its parent.
- For plain tagging use `tag=` on ports instead (see vlan-access-and-trunk-ports).

## Checked
2026-11-04. Confirmed against ovs-vsctl(8): Linux VLAN Bridging Compatibility section and the add-br, del-br, br-set-external-id, br-to-vlan and br-to-parent commands. Removed the `list-ports` remark, the `ovs-vsctl show` Verify line and the "gotcha" label that the page does not state.
Method: documentation only; no commands were run.
