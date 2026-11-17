---
id: computing-software.cloud-infrastructure-engineering.garage.inspect-and-purge-lost-blocks
name: inspect-and-purge-lost-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-block-list-errors, block-retry-now, block-purge, resync-errors]
level: advanced
status: docs-checked
description: "Triage blocks that cannot be fetched with block list-errors, info, retry-now and purge."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In very rare cases a block is unavailable from the whole cluster, so even `garage repair blocks` cannot fetch it. Each node keeps a list of block resync errors, the blocks whose last resync failed. View it with `garage block list-errors`.

The errors fall into three groups:

1. The block is still referenced but its object was deleted: a metadata reference inconsistency.
2. A non-deleted object references it, but the fetch failed for a transient reason such as a network failure.
3. A non-deleted object references it and no valid copy exists anywhere: a permanent error.

Use `garage block info` to see which objects reference a block, which separates case 1 from cases 2 and 3.

For transient errors Garage retries after a delay, so the error should clear itself. After fixing the cause, `garage block retry-now` asks for an immediate retry.

If you are sure the block is definitely lost (case 3), the only option is to declare the affected S3 objects unrecoverable and remove them properly with `garage block purge`.

For case 1, use the metadata reference fixes: `garage repair versions`, `block-refs` and `block-rc`.

## Checked

2026-11-04. Read the Durability & Repairs page in full. Confirmed list-errors, the three error categories, block info, retry-now, purge and the metadata reference repairs. Nothing removed.
Method: documentation only; no commands were run.
