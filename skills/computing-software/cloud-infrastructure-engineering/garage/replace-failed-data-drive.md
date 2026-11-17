---
id: computing-software.cloud-infrastructure-engineering.garage.replace-failed-data-drive
name: replace-failed-data-drive
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [disk-replacement, repair-blocks, resync-queue, garage-stats]
level: practitioner
status: docs-checked
description: "Replace a dead data disk when metadata survived by remounting a new disk and running garage repair blocks."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/recovering/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The recommended layout puts metadata on an SSD and blocks on an HDD. If only the HDD fails, blocks are lost but metadata is intact. The node does not need replacing and the configuration stays unchanged.

Steps:
1. Set up a new HDD as the data directory on the failed node.
2. Restart Garage with the existing configuration.
3. Run `garage repair -a --yes blocks`. This resyncs missing blocks onto the new drive from copies on other nodes.
4. Follow progress with `garage stats -a` and look for the block manager line `resync queue length`. It falls to zero when the node is fully synchronised.

The recovering page says the node does not need to be fully replaced and its configuration does not change. The configuration page describes `metadata_dir` as holding the node identifier, and in this scenario that directory is intact.

The known-issues page says resync defaults are conservative; when the resync queue is large with few resync errors, increase `resync-worker-count` and reduce `resync-tranquility` with `garage worker set`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Recovering from failures, Known issues. Confirmed on the recovering page: steps, `garage repair -a --yes blocks`, `garage stats -a` and the resync queue length output. Confirmed on the configuration page: `metadata_dir` holds the node identifier. Confirmed on the known-issues page: conservative resync defaults. Removed: the unsupported claim that no partitions are reassigned.

Method: documentation only; no commands were run.
