---
id: computing-software.cloud-infrastructure-engineering.garage.replication-factor-setting
name: replication-factor-setting
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [replication-factor, failure-tolerance, zones, cluster-sizing]
level: practitioner
status: docs-checked
description: "Choose replication_factor 1, 2, 3 or more and understand what failures each value survives."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`replication_factor` (since v1.0.0) can be any positive integer up to the node count. It strongly affects failure tolerance and performance.

- `1`: data lives on one node, with no redundancy. Use it only for test deployments.
- `2`: two copies on different nodes, ideally in different zones. One node failure, or several failures inside one zone, loses nothing. With a node down, data stays readable but writes fail.
- `3`: three copies, ideally in three zones. Two node failures, or failures in no more than two zones (given three or more zones), lose nothing. A single failed node, or failures within one zone, leave reading and writing working normally.
- `5`, `7`, and so on: choose an odd value, because every two extra copies lets one more node fail before reads and writes are lost.

Every node must carry the same `replication_factor`; never run a cluster where they differ.

Changing it is dangerous and not officially supported. The documented procedure is to shut the whole cluster down, delete the `cluster_layout` files in every metadata directory, update all config files, restart, and build a new layout with all kept nodes. A full rebalance follows, data may look unavailable meanwhile, and the page advises closing public access during it.

The known-issues page adds that one factor covers both data and metadata, so avoid `replication_factor = 1`.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Known issues. Confirmed on the configuration page: each value's behaviour, odd values above 3, same value on all nodes, the unsupported change procedure. Confirmed on the known-issues page: one factor for data and metadata, avoid 1. No changes needed.

Method: documentation only; no commands were run.
