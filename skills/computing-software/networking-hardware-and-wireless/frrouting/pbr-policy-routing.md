---
id: computing-software.networking-hardware-and-wireless.frrouting.pbr-policy-routing
name: pbr-policy-routing
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, pbrd, pbr, policy-based-routing, pbr-map, nexthop-group, fwmark]
level: advanced
status: docs-checked
description: "Configure FRR pbrd policy-based routing: pbr-map sequences with match and set, nexthop and VRF actions, pbr-policy on interfaces, table range and Linux kernel provider limits."
sources:
  - https://docs.frrouting.org/en/latest/pbr.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy-based routing (pbrd)
Map: `pbr-map NAME seq (1-700)` enters a sequence submode.

Match:
- `match src-ip|dst-ip PREFIX`, `match src-port|dst-port (1-65535)`, `match ip-protocol NAME` (from /etc/protocols).
- `match mark (1-4294967295)` (Linux, maps to `ip rule fwmark`), `match dscp (NAME|0-63)` (one per rule), `match ecn (0-3)`.
- `match pcp` and `match vlan` are ignored by the default Linux kernel dataplane provider unless another provider is used.

Set:
- `set nexthop-group NAME`.
- `set nexthop [A.B.C.D|X:X::X:X|blackhole] [interface] [nexthop-vrf NAME]`.
- `set vrf unchanged|NAME` (not with the NETNS VRF backend).
- `set queue-id`, `set pcp`, `set vlan`, `strip vlan`, `set src-ip|dst-ip`, `set src-port|dst-port`, `set dscp`, `set ecn` are ignored by the default Linux kernel dataplane provider (it does not support packet mangling).

Apply: under `interface NAME`, `pbr-policy MAP`. Sub-interfaces such as VLANs must be configured explicitly.

Tables: `pbr table range (10000-4294966272) (10000-4294966272)` sets the table IDs for new nexthop-group tables; configure before adding nexthop groups, existing tables are not resized.

Show: `show pbr map [NAME] [detail]`, `show pbr nexthop-groups [NAME]`, `show pbr interface [NAME]` (all accept `json`). Debug: `debug pbr events|map|nht|zebra`.

PBR works only on Linux. Internally a pbr-map becomes an `ip rule` that points at a table, and a nexthop or nexthop-group becomes a table with a default route via the nexthops.

## Checked

2026-11-08. Read the whole FRR PBR page: pbr-map sequence range, match and set commands and ranges, which ones the Linux kernel provider ignores, pbr-policy on sub-interfaces, table range, show and debug commands, PBR details. Reworded unsupported actions to ignored, as the page states.
Method: docs-only read of cited pages, 2026-11-08
