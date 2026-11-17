---
id: computing-software.cloud-infrastructure-engineering.garage.replace-node-with-lost-metadata
name: replace-node-with-lost-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [layout-assign-replace, new-node-id, lost-metadata, node-replacement]
level: advanced
status: docs-checked
description: "Replace a node whose metadata directory was lost using garage layout assign --replace."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/recovering/
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When a whole node dies, or only its metadata directory is lost, the replacement starts from an empty metadata directory and Garage generates a new node ID. The old ID must be replaced in the layout. Keeping an intact data directory is allowed but not necessary; data is rebalanced anyway and the replacement will not hold the same pieces, so most kept files would be deleted.

Procedure:
1. Prepare a new metadata drive (SSD recommended) and a data directory if needed, then start Garage on the new node.
2. `garage status` lists the new node as `NO ROLE ASSIGNED`, and the lost node's ID appears among disconnected or unavailable nodes.
3. Replace the old node:

`garage layout assign <new_node_id> --replace <old_node_id> -c <capacity> -z <zone> -t <node_tag>`

4. `garage layout show` to review, then `garage layout apply` (the layout page says apply takes `--version <new_version_number>`, 1 plus the previous version).

Garage then synchronises required data to the new node. Monitor with `garage stats -a`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Recovering from failures, Cluster layout management. Confirmed on the recovering page: new node ID, `NO ROLE ASSIGNED`, the `--replace` command with `-c`, `-z`, `-t`, review and apply, data rebalancing, `garage stats -a`. Added from the layout page: the apply `--version` requirement.

Method: documentation only; no commands were run.
