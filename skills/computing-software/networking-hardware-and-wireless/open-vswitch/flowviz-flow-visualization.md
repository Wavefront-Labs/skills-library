---
id: computing-software.networking-hardware-and-wireless.open-vswitch.flowviz-flow-visualization
name: flowviz-flow-visualization
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-flowviz, flow-visualization, flowviz, openflow, datapath, filter, ovn-detrace]
level: practitioner
status: draft
description: "Read large Open vSwitch flow dumps with ovs-flowviz: openflow and datapath subcommands, logic, tree, html and graph views, -f filter expressions and --ovn-detrace."
sources:
  - https://docs.openvswitch.org/en/latest/topics/ovs-flowviz/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ovs-flowviz
Input is a flow dump from a file (`-i flows.txt`) or stdin.

OpenFlow flows:
`ovs-flowviz -i flows.txt -f "table=8 and n_packets>0" openflow logic`
Add `--ovn-detrace` to annotate OVN logical flows.

Datapath flows:
`ovs-appctl dpctl/dump-flows | ovs-flowviz -f "output.port=2" datapath tree`
Datapath also has `html` and `graph` views.

Filters (`-f`): expressions on fields and counters combined with `and`, `or`, e.g. `table=8 and n_packets>0`.

Verify: re-run the same filter on a fresh dump; counters in `n_packets>0` should shrink the output to flows that saw traffic.

Gotcha: in `tree` and `logic` views a matching flow keeps its whole subtree, so a filtered view can still show non-matching children.
