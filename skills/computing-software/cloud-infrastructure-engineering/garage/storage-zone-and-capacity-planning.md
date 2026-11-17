---
id: computing-software.cloud-infrastructure-engineering.garage.storage-zone-and-capacity-planning
name: storage-zone-and-capacity-planning
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [zones, capacity, layout-assign-tags, three-zone-deployment]
level: practitioner
status: docs-checked
description: "Set zone names and capacities in the layout so Garage's failure guarantees apply."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/recovering/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/quick-start/
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage's failure guarantees depend on the layout knowing where nodes are. With 3-way replication across three or more zones, the cluster keeps working if failures are limited to one zone, and loses no data if failures stay within two zones. That requires each node to be assigned its real zone.

Set it when you add the node:

`garage layout assign -z <zone> -c <capacity> -t <tag> <node_id>`

- `-z` the zone, for example a datacenter.
- `-c` the capacity, which for a storage node is the space available in its data directory (the configuration page says the space available for `data_dir` is what you count).
- `-t` a tag, repeated for each tag.

`garage status` shows the Zone, Capacity and Tags columns, and shows `NO ROLE ASSIGNED` for nodes lacking a role. Use it to confirm each node is in the intended zone.

Capacity also influences distribution: the layout page's first example shows that a new node added to a zone gets no data when the other zones already hold full copies, while giving each of the two nodes in that zone half the capacity makes Garage share the data.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Quick Start, Recovering from failures, Cluster layout management, Known issues. Confirmed on the recovering page: the zone guarantees and `garage status` check. Confirmed on the Quick Start: `-z` and `-c` on `garage layout assign`. Confirmed on the configuration page: `data_dir` space counts toward capacity. Confirmed on the known-issues page: repeated `-t`. Confirmed on the layout page: the capacity example. Reworded the example sentence to match it.

Method: documentation only; no commands were run.
