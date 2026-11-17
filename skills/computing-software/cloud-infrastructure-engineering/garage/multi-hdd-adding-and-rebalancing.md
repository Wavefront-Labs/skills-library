---
id: computing-software.cloud-infrastructure-engineering.garage.multi-hdd-adding-and-rebalancing
name: multi-hdd-adding-and-rebalancing
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [multi-hdd, lazy-rebalancing, garage-repair-rebalance, secondary-directories]
level: advanced
status: docs-checked
description: "Add storage locations without immediate rebalancing, then rebalance lazily or actively."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/multi-hdd/
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Adding a location to `data_dir` does not rebalance existing data. New blocks are balanced by capacity, and existing blocks move only opportunistically when re-written, for instance when an object is re-uploaded or an upload contains a duplicate block.

Two strategies balance the drives:

- Lazy rebalancing: when a block is re-written, Garage checks whether the current copy sits in the slice's primary directory. If it is in a secondary one, Garage writes a copy to the primary and deletes the old one. This may never finish when some blocks are only read, never rewritten.
- Active rebalancing: run `garage repair rebalance`. It moves all blocks to their primary location. Afterwards all secondary locations are removed, so Garage no longer searches them, and each block has one possible location, which can speed up access.

The durability page notes this is useful when adding locations or changing capacities, and that the operation also moves everything out of read-only locations.

Use `garage repair -a --yes rebalance` to run across nodes.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Durability & Repairs, Multi-HDD support. Confirmed on the multi-HDD page: no automatic rebalance on adding locations, lazy and active rebalancing, secondary locations removed afterwards. Confirmed on the durability page: `garage repair rebalance`, its use when adding locations or changing capacities, and moving data out of read-only locations; `-a --yes` flags. No claims removed.

Method: documentation only; no commands were run.
