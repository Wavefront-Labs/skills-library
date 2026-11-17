---
id: computing-software.networking-hardware-and-wireless.frrouting.administrative-distance-and-route-replace
name: administrative-distance-and-route-replace
category: computing-software
field: networking-hardware-and-wireless
product: frrouting
tags: [networking-hardware-and-wireless, frrouting, zebra, administrative-distance, kernel-metric, route-replace, import-table]
level: advanced
status: docs-checked
description: "FRR default administrative distances, what distance 255 means, kernel route metric 20 and replace semantics, and importing alternate kernel tables into the RIB."
sources:
  - https://docs.frrouting.org/en/latest/zebra.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Administrative distance and route replace
Lower distance wins. Listed values: system, kernel, connect 0; static 1; NHRP 10; EBGP 20; EIGRP 90; Babel 100; OSPF 110; IS-IS and OpenFabric 115; RIP 120; Table and SHARP 150; IBGP and PBR 200.

- Distance 255 means the route is not installed in the dataplane and not redistributed, except kernel routes, which are redistributed even at 255.
- For non-FRR kernel routes, the top byte of the metric is read as admin distance and the low three bytes as metric.
- Kernel routes installed by FRR use metric 20. The kernel metric is unrelated to the RIB metric or distance; it only breaks ties between routing suites.
- Route-replace needs the same metric on the replace command and is Linux-only. `--v6-rr-semantics` uses replace for IPv6 instead of delete-then-add (needs kernel support).

Table import and allocation:
- `ip import-table (1-252) [mrib] [distance (1-255)] [route-map RMAP_NAME]` continuously syncs routes from an alternate table into the unicast RIB (or the multicast RIB with `mrib`). `ipv6 import-table` is the IPv6 form.
- `ip table range STARTTABLENO ENDTABLENO` reserves kernel tables for other services such as BGP flowspec, avoiding VRF table conflicts.

## Checked

2026-11-08. Read the FRR zebra page: administrative distance table, distance 255 handling, kernel metric decoding, metric 20 and route replace semantics, --v6-rr-semantics, import-table and table range. Nothing changed.
Method: docs-only read of cited pages, 2026-11-08
