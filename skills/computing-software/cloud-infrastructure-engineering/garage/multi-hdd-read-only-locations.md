---
id: computing-software.cloud-infrastructure-engineering.garage.multi-hdd-read-only-locations
name: multi-hdd-read-only-locations
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [read-only-data-dir, drain-drive, remove-data-directory, find-type-f]
level: advanced
status: docs-checked
description: "Drain and retire a data directory by marking it read_only and rebalancing."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/multi-hdd/
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To move all blocks off an existing data directory, mark it read-only and add the new locations:

`data_dir = [ { path = "/path/to/old_data", read_only = true }, { path = "/path/to/new_hdd1", capacity = "2T" }, { path = "/path/to/new_hdd2", capacity = "4T" } ]`

Garage can still read requested blocks from the read-only directory. It moves data out progressively through lazy rebalancing, or at once when you request active rebalancing with `garage repair rebalance`.

When the active rebalance has finished, the read-only directory should hold no data files. Subdirectories may remain. Verify with a file search such as `find /path/to/old_data -type f`, which must print nothing. Only then remove the entry from `data_dir` in the configuration.


In the page's example the old location is listed first with `read_only = true` and no `capacity`, followed by two new locations with capacities of 2T and 4T.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Durability & Repairs, Multi-HDD support. Confirmed: the `read_only = true` example, reads still served from the old directory, lazy and active rebalancing, the empty-of-files check, and removal afterwards. Confirmed on the durability page that `garage repair rebalance` moves data out of read-only locations. Removed: the claim that a read-only entry cannot have a capacity because nothing new is written (the page only shows an example without one). The page's `find` example puts the path after `-type f`; the skill keeps the path first, which is the portable order, and says 'such as'.

Method: documentation only; no commands were run.
