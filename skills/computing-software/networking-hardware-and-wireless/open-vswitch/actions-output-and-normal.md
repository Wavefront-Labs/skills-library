---
id: computing-software.networking-hardware-and-wireless.open-vswitch.actions-output-and-normal
name: actions-output-and-normal
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, output, normal, flood, in-port, controller-action, group-action, bundle-action, drop, openflow-actions]
level: practitioner
status: docs-checked
description: "Forward packets from OpenFlow flows in Open vSwitch with the output, normal, flood, in_port, controller, group and bundle actions, and drop by leaving actions empty."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-actions.7/
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - https://docs.openvswitch.org/en/latest/faq/openflow/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# actions: output and normal
Forwarding actions in a flow's `actions=` list:
- `output:port` (or just `port`) sends to an OpenFlow port; if the port is the packet's input port, the packet is not output. `output(port=port,max_len=nbytes)` truncates the packet to at most `nbytes` bytes for that one output only (the output port may not be a patch port); meant for monitoring and mirroring to a collector.
- `normal` subjects the packet to the device's normal L2/L3 processing; in OVS this is the "normal pipeline" driven by the Open_vSwitch database (VLAN mode, bonding, MAC learning, mirrors).
- `flood` outputs on all physical ports except the input port and ports with flooding disabled (STP/RSTP can disable it, as can `ovs-ofctl mod-port`). `all` is the same without the flooding-disabled exception.
- `in_port` outputs on the port the packet arrived on; it is the standard way to hairpin, for example `ovs-ofctl add-flow br0 in_port=2,actions=in_port`.
- `controller(...)` sends a packet-in to the controller, with options `max_len=`, `reason=`, `id=`, `userdata=`, `pause`. From OVS 2.7 `max_len` has no effect: the whole packet is always sent.
- `group:N` outputs to OpenFlow group N, which must exist or OVS refuses to add the flow (see ofctl-group-tables).
- `bundle(fields,basis,algorithm,ofport,members:port...)` picks one live member port by `active_backup` or `hrw` and outputs to it; `bundle_load` writes the port number to a field instead.
- `enqueue(port,queue)` exists in OpenFlow 1.0 only; OVS translates it to `set_queue`, `output`, `pop_queue` in later versions.
- A packet that meets no output action in the pipeline is effectively dropped.

Examples:
`ovs-ofctl add-flow br0 priority=0,actions=normal`
`ovs-ofctl add-flow br0 in_port=1,actions=output:2,output:3`

Actions run in order, so a packet modification not eventually followed by an output action has no externally visible effect.

## Checked
2026-11-04. Confirmed against ovs-actions(7): output, The OVS Normal Pipeline, controller, enqueue, bundle and group sections. Removed the claim that `max_len` truncates what goes to a controller port (page says it truncates the output for that action), the "slave" wording, the unsourced `drop` keyword claim, and the Verify line about trace output.
Method: documentation only; no commands were run.
