---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ofctl-add-and-dump-flows
name: ofctl-add-and-dump-flows
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, add-flow, dump-flows, add-flows, ovs-ofctl, priority, table, names]
level: intro
status: docs-checked
description: "Install and list OpenFlow flows with ovs-ofctl: add-flow, add-flows from a file or stdin, dump-flows filters, default priority 32768, table numbers, dropping with empty actions."
sources:
  - http://www.openvswitch.org/support/dist-docs/ovs-ofctl.8.txt
  - https://docs.openvswitch.org/en/latest/faq/openflow/
  - https://docs.openvswitch.org/en/latest/tutorials/faucet/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ofctl add and dump flows
Syntax (ovs-ofctl(8)):
```
ovs-ofctl [--bundle] add-flow switch flow
ovs-ofctl [--bundle] add-flow switch - < file
ovs-ofctl [--bundle] add-flows switch file
ovs-ofctl dump-flows switch [flows]
```
Each flow line in a file may start with `add`, `modify`, `delete`, `modify_strict` or `delete_strict`; without a keyword it is an add. Flow mods run in the order given.

Examples:
- `ovs-ofctl add-flow br0 "table=1 priority=0 actions=flood"` (from the ovs-ofctl(8) learn example)
- `ovs-ofctl add-flow br0 in_port=2,actions=in_port` (hairpin; OpenFlow otherwise ignores output to the ingress port)
- `ovs-ofctl add-flow br0 ip,nw_dst=192.168.0.1,actions=drop`

Flow fields:
- `priority` 0 to 65535, default 32768 when adding; higher matches first. Behaviour is undefined when several flows of the same priority can match one packet (OVS does not make more specific flows win).
- `table` selects the table; with OpenFlow 1.1 and later, if omitted (or 255) ovs-ofctl uses table 0.
- `actions=` must be the final field. An empty list drops: `priority=65535,actions=` is the same as `actions=drop`.
- `idle_timeout` and `hard_timeout` in seconds (0, the default, never expires), `cookie`, `importance` (OpenFlow 1.4+), `send_flow_rem`, `check_overlap`, `reset_counts`.

An L3 field needs its protocol in the match (`ip,nw_dst=...` or `arp,nw_dst=...`); otherwise the L3 match is dropped by normalization and the flow matches every packet.

Dumping: `dump-flows switch [flows]` prints the OpenFlow flows matching the filter, in switch order unless sorted. Options:
- `--sort[=field]` and `--rsort[=field]` order the output by a match field, or by priority if omitted.
- `--names`/`--no-names` accept and display port and table names; names are displayed by default only on an interactive console.
- `--stats`/`--no-stats`: `--no-stats` drops duration, packet and byte counts and ages, and also cookie and table values when zero.
- `-O OpenFlow13` selects protocol versions (needed for later versions; see openflow-versions). The Faucet tutorial uses `ovs-ofctl -OOpenFlow13 --names --no-stat dump-flows br0`.

Gotcha: `ovs-dpctl dump-flows` queries a kernel datapath, not the OpenFlow tables, so it will not show flows you added with ovs-ofctl; use `ovs-ofctl dump-flows`. `ovs-appctl dpif/dump-flows br` shows the datapath flows in ongoing traffic.

## Checked
2026-11-04. Confirmed against ovs-ofctl(8) (flow table commands, priority, options), the OpenFlow FAQ (normalization, drop, hairpin, dpctl) and the Faucet tutorial helper line. Removed the unsourced "a restrictive IP-only flow also drops ARP" gotcha and the Verify line about `n_packets`; the stdin form is shown for `add-flow`.
Method: documentation only; no commands were run.
