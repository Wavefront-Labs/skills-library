---
id: computing-software.cloud-infrastructure-engineering.garage.garage-repair-command-syntax
name: garage-repair-command-syntax
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [garage-repair, repair-yes-flag, repair-all-nodes, repair-operations]
level: practitioner
status: docs-checked
description: "Run repair operations with the required --yes flag and the -a flag to cover every node."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/durability-repairs/
  - https://garagehq.deuxfleurs.fr/documentation/operations/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage repairs have the form `garage repair <repair_name>`. They refuse to start without confirmation, so add `--yes`:

`garage repair --yes <repair_name>`

By default a repair runs only on the node your CLI connects to. To run on all nodes, add `-a` (also written `--all-nodes`):

`garage repair -a --yes <repair_name>`

Names covered by the durability page:

- `scrub` (with `start`, `pause` and related subcommands) verifies block hashes.
- `blocks` checks block references against disk contents.
- `rebalance` moves blocks between data directories.
- `tables` resyncs metadata tables.
- `versions`, `block-refs` and `block-rc` fix metadata reference inconsistencies.

Progress can be followed with `garage worker list` (repair workers show a Done state when finished) and `garage worker info <task_id>`. The upgrade page recommends `garage repair --all-nodes --yes tables` before upgrading, calling it very quick (under a minute), and then confirming completion in the daemon logs or `garage worker list`.

## Checked

2026-11-04. Read the Durability & Repairs and Upgrading pages in full. Confirmed the --yes and -a rules, the repair names, the worker commands and the upgrade-page advice. Removed the garage stats paragraph, which neither page states.
Method: documentation only; no commands were run.
