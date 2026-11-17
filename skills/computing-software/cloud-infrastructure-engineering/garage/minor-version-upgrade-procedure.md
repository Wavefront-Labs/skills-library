---
id: computing-software.cloud-infrastructure-engineering.garage.minor-version-upgrade-procedure
name: minor-version-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [upgrading-garage, minor-upgrade, rolling-upgrade, garage-build-info]
level: practitioner
status: docs-checked
description: "Upgrade Garage nodes one at a time for minor releases, with no downtime, after a health check."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Garage nodes share data structures, so upgrades need care. The version identifier tells you the kind: a major upgrade bumps the first nonzero component (v0.7.2 to v0.8.0), a minor upgrade keeps it (v0.8.0 to v0.8.1). Major upgrades only work between contiguous versions: v0.7.0 to v0.8.2 is supported, v0.6.0 to v0.8.0 is not.

The Prometheus metric `garage_build_info` shows which versions run in the cluster.

Minor upgrades need no downtime. Read the changelog and ideally test on a staging cluster. Then:

1. Check health. At least run `garage repair --all-nodes --yes tables` (under a minute) and confirm it finished in the daemon logs, or via `garage worker list` showing the repair workers as Done.
2. Upgrade nodes one by one: stop it, install the new binary, edit the configuration if needed, restart it.

Major upgrades are handled separately, with per-upgrade guides under the Working Documents section; the page stresses reading the changelog and ideally testing on a staging cluster before any upgrade.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Upgrading Garage. Confirmed: major versus minor version rule and the contiguous-version examples, `garage_build_info`, no downtime for minor upgrades, `garage repair --all-nodes --yes tables` (under a minute), `garage worker list` Done state, and the node-by-node procedure. No changes needed.

Method: documentation only; no commands were run.
