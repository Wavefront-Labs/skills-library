---
id: computing-software.cloud-infrastructure-engineering.garage.multi-hdd-data-dir-setup
name: multi-hdd-data-dir-setup
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [multi-hdd, data-dir-list, capacity-proportional, hash-slices]
level: practitioner
status: docs-checked
description: "Configure several data drives per node with a data_dir list and capacities, and know how blocks are placed."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/multi-hdd/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Since v0.9 Garage supports nodes with several drives for data blocks, though not for metadata. Format and mount each drive in its own directory, then list them:

`data_dir = [ { path = "/path/to/hdd1", capacity = "2T" }, { path = "/path/to/hdd2", capacity = "4T" } ]`

Garage balances blocks automatically in proportion to the capacities.

How placement works: all possible block hashes are divided into a fixed number of slices (currently 1024), each assigned a primary location, with slice counts proportional to capacity. A new block is always written to the primary directory of the slice containing its hash.

Garage also keeps a list of secondary directories per slice, i.e. places that were once primary and might still hold blocks. Reads check the primary first and then the secondaries until the block is found. That is what lets Garage keep working when locations are added without shuffling files.

The configuration page says the space available for `data_dir` should be counted to determine a node's capacity when adding it to the cluster layout.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Configuration file format, Multi-HDD support. Confirmed: support since v0.9 for data blocks only, the `data_dir` list syntax, proportional balancing, 1024 slices, primary and secondary directories, read order. Changed: the layout capacity statement is now worded as the configuration page words it.

Method: documentation only; no commands were run.
