---
id: computing-software.cloud-infrastructure-engineering.garage.recover-by-removing-a-failed-node
name: recover-by-removing-a-failed-node
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [node-failure, layout-remove, availability-zones, three-zone-guarantees]
level: practitioner
status: docs-checked
description: "Survive a dead node by removing it from the layout when you lack spares and have at least three remaining nodes."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/recovering/
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
With three or more zones and 3-way replication (the recommended mode), Garage guarantees that the cluster stays fully functional while failing machines are in only one zone (including a whole zone losing power or Internet), and that no data is lost while failures are confined to at most two zones. This only holds if each node is configured with its correct zone; check with `garage status`.

Temporarily disconnected nodes resynchronise automatically on return.

If a disk dies and you have no replacement parts, and at least three other nodes remain, simply drop the node from the layout:

`garage layout remove <node_id>`
`garage layout show`
`garage layout apply`

The layout page says `garage layout apply` takes `--version <new_version_number>`, which must be 1 plus the previous layout version, and that you should review `garage layout show` first. Get the ID from `garage status`. This repartitions data so three copies of everything exist on the remaining nodes.

If you do plan to replace the failed part with new hardware, the page does not recommend removing and then re-adding the node (it should work), and points to the replacement scenarios instead.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Recovering from failures, Cluster layout management. Confirmed on the recovering page: the three-zone guarantees, `garage status` zone check, automatic resync of temporary disconnections, the removal commands and the 'at least 3' remaining nodes condition, and the advice against remove-then-re-add. Added from the layout page: the `--version` requirement of `garage layout apply`.

Method: documentation only; no commands were run.
