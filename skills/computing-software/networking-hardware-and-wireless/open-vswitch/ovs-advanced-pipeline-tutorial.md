---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovs-advanced-pipeline-tutorial
name: ovs-advanced-pipeline-tutorial
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-sandbox, tutorial, multi-table, mac-learning, pipeline, sandbox, ofproto-trace, pcap]
level: practitioner
status: draft
description: "Practise Open vSwitch in ovs-sandbox by building a five-table pipeline: admission, VLAN input, MAC learning with learn(), lookup and output, then test with ofproto/trace."
sources:
  - https://docs.openvswitch.org/en/latest/tutorials/ovs-advanced/
  - http://www.openvswitch.org/support/dist-docs/ovs-sandbox.1.txt
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Advanced pipeline tutorial
Environment: `ovs-sandbox` (also `./ovs-sandbox -b DIR`, or `make sandbox` from a source tree) starts private daemons without touching the host.

Setup:
```
ovs-vsctl add-br br0 -- set Bridge br0 fail-mode=secure
ovs-vsctl add-port br0 p1 -- set Interface p1 ofport_request=1
ovs-ofctl mod-port br0 p1 up
```
Repeat for more ports, using `ofport_request` for stable numbers.

Pipeline design:
- Table 0: admission control.
- Table 1: VLAN input.
- Table 2: learn source MACs: `learn(table=10, NXM_OF_VLAN_TCI[0..11], NXM_OF_ETH_DST[]=NXM_OF_ETH_SRC[], load:NXM_OF_IN_PORT[]->NXM_NX_REG0[0..15])`.
- Table 3: look up the destination in table 10.
- Table 4: output.

Test each stage with `ovs-appctl ofproto/trace br0 in_port=p1,dl_src=...` (add `--generate` so learning applies).

Capture traffic: `ovs-vsctl set interface p1 options:pcap=p1.pcap`.

Verify: after a trace with `--generate`, `ovs-ofctl dump-flows br0 table=10` shows the learned entry.

Gotcha: `fail-mode=secure` means no flows, no forwarding; add the table 0 flow before testing.
