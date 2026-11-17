---
id: computing-software.networking-hardware-and-wireless.frrouting.bgp-peer-groups-and-listen-ranges
name: bgp-peer-groups-and-listen-ranges
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, bgpd, peer-group, listen-range, dynamic-neighbors, update-groups, optmem-max]
level: practitioner
status: docs-checked
description: "Use FRR BGP peer groups and bgp listen range for dynamic neighbors, set the listen limit, and view update groups and peer-group state."
sources:
  - https://docs.frrouting.org/en/latest/bgp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP peer groups and listen ranges
- `neighbor WORD peer-group` defines a peer group; `neighbor PEER peer-group PGNAME` adds a peer.
- `bgp listen range <A.B.C.D/M|X:X::X:X/M> peer-group PGNAME` accepts connections from any peer in the prefix, using the group's configuration.
- `bgp listen limit <1-65535>` caps accepted peers per instance (default 100); the file-descriptor limit can also cap it.
- With TCP MD5 on the group, Linux needs kernel 4.14 or later; otherwise the range accepts only peers without MD5. At several hundred peers the kernel may hit its option memory limit; raise `net.core.optmem_max`.
- `neighbor PEER solo` prevents routes being reflected back to the peer.
- `show [ip] bgp peer-group [json]` displays groups.
- `coalesce-time (0-4294967295)` sets the delay in ms before peers are grouped into update groups (default 1000).
- Update groups: `show bgp update-groups [advertise-queue|advertised-routes|packet-queue]`, `show bgp update-groups statistics`; `debug bgp update-groups`.
- `neighbor PEER maximum-prefix-out NUMBER` creates a separate update group.

## Checked
2026-11-09. Partial read of docs.frrouting.org bgp.html (one large page): the listen range and listen limit section (kernel 4.14, optmem_max, default 100, ulimit), coalesce-time, maximum-prefix-out, solo, show bgp peer-group and show bgp update-groups. Nothing removed.
Method: documentation only; no commands were run.
