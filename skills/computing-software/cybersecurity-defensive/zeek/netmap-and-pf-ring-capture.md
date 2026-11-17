---
id: computing-software.cybersecurity-defensive.zeek.netmap-and-pf-ring-capture
name: netmap-and-pf-ring-capture
category: computing-software
field: cybersecurity-defensive
product: zeek
tags: [cybersecurity-defensive, zeek, netmap, pf-ring, flow-balancing, packet-source]
level: advanced
status: docs-checked
description: "Alternative Zeek packet sources: netmap syntax, lb pipes on FreeBSD, the zeek-netmap double-colon form, and PF_RING versus AF_PACKET."
sources: ["https://docs.zeek.org/en/current/cluster-setup.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# netmap and pf-ring capture

**Frontend options**: cPacket devices do layer-2 load balancing by rewriting destination MACs, with a BPF filter per worker. PF_RING clustering balances flows across processes sniffing one interface. Unless you specifically need PF_RING, try AF_PACKET first because it needs no out-of-tree kernel module.

**netmap on FreeBSD**: libpcap supports it.

```
zeek -i netmap:em0
```

This puts the interface into kernel-bypass mode, which can disable normal networking including SSH if it is your primary interface. Multi-ring NICs: `netmap:em0-0`, `netmap:em0-1`.

Software balancing uses the `lb` tool from `/usr/src/tools/tools/netmap/`:

```
lb -i em0 -p zeek:4
```

Workers then attach to the pipes with the `/x` exclusive suffix. `tcpdump -i netmap:zeek}1/r` attaches a read monitor.

**zeek-netmap plugin**: the interface spec gains a colon, for example `netmap::zeek}0/x`. It is required on Linux (with the out-of-tree netmap kernel module) unless libpcap has native netmap support: `zeek -i netmap::eth1`.

## Checked

2026-11-08: read in full against the documentation source(s) listed in sources; the claims, names, values and examples in this skill match the page text.

Method: documentation only; no commands were run.
