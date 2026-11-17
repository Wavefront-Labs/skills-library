---
id: computing-software.cloud-infrastructure-engineering.garage.resync-tuning-and-layout-history
name: resync-tuning-and-layout-history
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [resync-tranquility, resync-worker-count, garage-worker-set, layout-history]
level: advanced
status: docs-checked
description: "Speed up a backed-up resync queue with worker settings and diagnose stuck layout versions."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Resync tranquility is conservative by default. The worker parameters `resync-tranquility` and `resync-worker-count` start at very cautious values to avoid overloading nodes with I/O, but the resync queue can then grow faster than it empties, causing performance problems elsewhere. The sign is a large resync queue with few resync errors, meaning the queue is not caused by a disconnected or faulty node.

Fix by raising workers and lowering tranquility. To resync as fast as possible:

`garage worker set -a resync-worker-count 8`
`garage worker set -a resync-tranquility 0`

Both commands are shown with the `-a` flag in the page.

Layout updates can need manual intervention. If disconnected nodes are removed and replaced in the layout, Garage may refuse to evict the old nodes, a built-in safeguard against inconsistent state. Several layout versions then remain active even after a full resync. Diagnose with `garage layout history`, which prints instructions to fix it.

Tags: in `garage layout assign`, repeat `-t` for each tag; a comma-separated list becomes a single string tag.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Known issues. Confirmed: conservative defaults, large queue with few errors, the two `garage worker set` commands, `garage layout history`, the eviction safeguard, repeated `-t`. Removed: the claim that `-a` applies the setting to all nodes (the page does not explain the flag for `worker set`).

Method: documentation only; no commands were run.
