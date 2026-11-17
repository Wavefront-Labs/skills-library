---
id: computing-software.networking-hardware-and-wireless.open-vswitch.ovs-tcpdump-mirror
name: ovs-tcpdump-mirror
category: computing-software
field: networking-hardware-and-wireless
product: open-vswitch
tags: [networking-hardware-and-wireless, open-vswitch, ovs-tcpdump, span-capture, tcpdump, mirror, capture]
level: intro
status: docs-checked
description: "Capture traffic from an Open vSwitch port with ovs-tcpdump: syntax, --mirror-to, --span, --filter, --db-sock, automatic mirror creation and cleanup, and privileges."
sources:
  - https://docs.openvswitch.org/en/latest/ref/ovs-tcpdump.8/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ovs tcpdump mirror
`ovs-tcpdump -i <port> <tcpdump options>...`

It creates a mirror port in ovs-vswitchd, runs tcpdump on it, and removes the mirror it created when tcpdump exits. It will not create a second mirror for the same port (it checks the existing configuration first).

Options:
- `-i`, `--interface`: port to mirror and dump; may appear only once.
- `--mirror-to`: interface that receives the mirrored packets; created if missing, otherwise it must be a port type tcpdump can use. Default `mi<port>`.
- `--span`: mirror all ports (optional).
- `--filter <flow>`: mirror only packets matching an OpenFlow filter; fields are in ovs-fields(7).
- `--db-sock <socket>`: database socket; default `unix:<rundir>/db.sock`.
- `--dump-cmd <command>`: run another command instead of tcpdump.
- Remaining arguments are the tcpdump options.

Gotcha: on Linux, tap devices receive packets only when an application has them open, which requires `CAP_NET_ADMIN`, normally root.

## Checked
2026-11-04. Confirmed against the ovs-tcpdump(8) page: synopsis, every option and default listed, mirror creation and cleanup, the duplicate-mirror check and the CAP_NET_ADMIN note. Removed because the page did not confirm them: the pcap example, the leftover-mirror check with `ovs-vsctl list mirror` and the cross-reference.
Method: documentation only; no commands were run.
