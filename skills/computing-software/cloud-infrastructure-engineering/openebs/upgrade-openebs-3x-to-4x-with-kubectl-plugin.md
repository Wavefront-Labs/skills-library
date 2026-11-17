---
id: computing-software.cloud-infrastructure-engineering.openebs.upgrade-openebs-3x-to-4x-with-kubectl-plugin
name: upgrade-openebs-3x-to-4x-with-kubectl-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [upgrade, helm, kubectl-openebs, partial-rebuild, mayastor, downgrade, migration]
level: advanced
status: docs-checked
description: "Upgrade OpenEBS 3.x to 4.6 with the kubectl openebs upgrade command, including the helm repo URL change and the partial-rebuild setting for data consistency."
sources:
  - https://openebs.io/docs/user-guides/upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The upgrade page targets OpenEBS 4.6, a unified installer for the Local PV engines plus Replicated PV Mayastor. After upgrading, the chart installs all four engines whatever you ran before; if you only want Local PV, pass `--set engines.replicated.mayastor.enabled=false`. **Downgrades are not supported.**

Supported paths: 3.x to 4.x only for storages that were installed from 3.x as Local PV Hostpath, LVM, ZFS, Rawfile or Replicated PV Mayastor. Other storages go through the migration documentation.

Steps for 3.x to 4.6:

1. The chart repository URL has changed. Run `helm repo remove openebs`, then `helm repo add openebs https://openebs.github.io/openebs`, then `helm repo update`.
2. Download the `kubectl openebs` binary from the OpenEBS GitHub releases.
3. Run `kubectl openebs upgrade -n <namespace>`.
4. Watch it with `kubectl openebs upgrade status -n <namespace>`.
5. Confirm CRDs, volumes, snapshots and storage pools were not affected.

For 3.x to 4.x, add `--set mayastor.agents.core.rebuild.partial.enabled=false` to the upgrade command to keep data consistent. If you disabled partial rebuild, turn it back on after a successful upgrade with `kubectl openebs upgrade -n <namespace> --set mayastor.agents.core.rebuild.partial.enabled=true`. The option is not needed for 4.x to newer upgrades.

## Checked

Method: 2026-11-08 read the raw markdown of the cited upgrade page in full; supported paths, steps and the partial-rebuild option match and are unchanged.
