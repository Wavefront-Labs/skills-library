---
id: computing-software.cloud-infrastructure-engineering.garage.block-repair-and-resync
name: block-repair-and-resync
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-repair-blocks, block-resync, block-reference-counter, layout-change-followup]
level: practitioner
status: docs-checked
description: "Use garage repair blocks to reconcile referenced blocks with what is stored on disk."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Sometimes a node holds a reference to a block it does not actually have on disk. The opposite happens too: blocks on disk that nothing references. `garage repair blocks` fixes both. It scans the entire block reference counter table to confirm referenced blocks exist on disk, and scans the whole disk store to confirm stored blocks are referenced.

When to run it:

- After changing the cluster layout, once the metadata tables have finished synchronising between nodes, usually a few hours after `garage layout apply`.
- After deleting a corrupted data file by hand (the configuration page says to follow the deletion with `garage repair blocks` so the node re-fetches the block from another node).

Repairs do not start without `--yes`. Add `-a` to cover all nodes; without it only the node the CLI connects to is repaired, for example `garage repair -a --yes blocks`.

If the resync queue grows faster than it clears, see the known issue on conservative resync tranquility.

## Checked

2026-11-04. Read the Durability & Repairs, Configuration file format and Known issues pages. Confirmed the two cases fixed by `garage repair blocks`, the layout-change timing, the post-deletion repair and the `--yes` and `-a` rules. Removed the drive-replacement bullet (command combination and `garage stats -a` not on these pages).
Method: documentation only; no commands were run.
