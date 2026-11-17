---
id: computing-software.cybersecurity-defensive.zeek.af-packet-load-balancing
name: af-packet-load-balancing
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, af-packet, fanout-id, ethtool-offload, lb-method]
level: advanced
status: docs-checked
description: "Capture with af_packet:: on Linux, fanout groups and AF_Packet::fanout_id, file capabilities, ethtool offload settings, and ZeekControl lb_method=af_packet."
sources: ["https://docs.zeek.org/en/current/cluster-setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# af-packet load balancing

AF_PACKET is supplied by the Zeek::AF_Packet plugin on Linux builds. Check it with `zeek -N Zeek::AF_Packet`. One worker:

```
zeek -i af_packet::eth0
```

Needs CAP_NET_RAW and CAP_NET_ADMIN; `sudo setcap cap_net_raw,cap_net_admin=+eip /path/to/zeek` lets an unprivileged user run it.

Disable NIC offloading so packets look as on the wire:

```
for offload in rx tx sg tso ufo gso gro lro; do ethtool -K $IFACE $offload off; done
```

Workers on the same interface join a fanout group and share traffic via symmetric flow hashes. The group id is `AF_Packet::fanout_id`, default 23. Two workers on different interfaces in one network namespace need distinct ids:

```
zeek -i af_packet::eth0 AF_Packet::fanout_id=23 &
zeek -i af_packet::eth1 AF_Packet::fanout_id=24 &
```

A worker crashing out of memory can briefly disturb balancing, giving gaps or duplicated connections.

ZeekControl node.cfg: `lb_method=af_packet`, `lb_procs=4`, `af_packet_fanout_id=20` (unique per interface), and `pin_cpus=4,5,6,7`.

## Checked

2026-11-04: read against the official Zeek documentation page(s) listed in sources; the claims, names, values and examples in this skill match the page text. Nothing else was added.

Method: documentation only; no commands were run.
