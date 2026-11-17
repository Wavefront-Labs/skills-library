---
id: computing-software.systems-network-administration.network-design.arping-layer-2-reachability
name: arping-layer-2-reachability
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, network-tools, arping, layer-2-testing, duplicate-ip, arp-process]
level: practitioner
status: docs-checked
description: "Use arping to test layer-2 reachability and find IP conflicts: probing hosts that block ICMP, duplicate address detection mode, gratuitous ARP, and iputils vs Habets versions."
sources:
  - https://man7.org/linux/man-pages/man8/arping.8.html
  - https://github.com/ThomasHabets/arping
  - https://www.rfc-editor.org/rfc/rfc5227
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# arping

arping sends ARP requests and reports replies, so it works even when hosts drop ICMP. Only on the
local L2 segment (does not cross routers).

## Two implementations
- **iputils arping** (most Linux distros' default): `arping -I eth0 10.0.0.1`.
- **Thomas Habets arping**: can also ping by MAC; options differ. Check `arping -V` / man page.
  (The iputils man page documents IPv4 only; for IPv6 it points to ndisc6.)

## Common uses (iputils)
```
arping -I eth0 -c 3 10.0.0.1            # is the gateway alive at L2; shows replying MAC
arping -D -I eth0 -c 2 10.0.0.50        # duplicate address detection: exit 0 if no replies arrive
arping -U -I eth0 -c 3 10.0.0.50        # unsolicited (gratuitous) ARP to update neighbours' caches
arping -A -I eth0 -c 3 10.0.0.50        # like -U but with ARP REPLY packets
arping -s 10.0.0.20 -I eth0 10.0.0.1    # set source IP
```

## Diagnostics
- **Replies from two different MACs** -> IP conflict; find each MAC in the switch MAC tables.
- Reply present but ping fails -> host firewall blocks ICMP; L2 path is fine.
- No reply -> wrong VLAN, host down, or a switch security feature dropping ARP.
- After a VIP failover, send `-U` to refresh upstream caches if the cluster software did not.

## Verify
- [ ] Before assigning a static IP, `arping -D` shows no existing owner; conflicts found are traced to a switch port.

## Checked
2026-10-28. Confirmed against the arping(8) man page: options `-A`, `-U`, `-D` (returns 0 if no replies), `-c`, `-I`, `-s` (source 0.0.0.0 in DAD mode, destination in unsolicited mode), `-V`, `-w` exit status; IPv4 only; and the Habets README (ping by MAC; works when the host blocks ICMP). Removed: the Windows equivalents section and the DAI remark, which the sources do not support.
Method: documentation only; no commands were run.
