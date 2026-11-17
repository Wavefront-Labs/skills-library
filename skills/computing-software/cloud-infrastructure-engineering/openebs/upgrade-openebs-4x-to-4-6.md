---
id: computing-software.cloud-infrastructure-engineering.openebs.upgrade-openebs-4x-to-4-6
name: upgrade-openebs-4x-to-4-6
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [upgrade, kubectl-openebs, helm, 4x, upgrade-status]
level: practitioner
status: docs-checked
description: "Upgrade an existing OpenEBS 4.x deployment to 4.6 with the kubectl openebs plugin, monitor it with upgrade status, and verify CRDs, volumes, snapshots and pools."
sources:
  - https://openebs.io/docs/user-guides/upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Upgrading within the 4.x line is shorter than the 3.x path. The documented steps for 4.x to 4.6:

1. Download the `kubectl openebs` binary from the OpenEBS releases page on GitHub.
2. Run `kubectl openebs upgrade -n <namespace>`.
3. Monitor with `kubectl openebs upgrade status -n <namespace>`.
4. Verify that the CRDs, volumes, snapshots and storage pools are unaffected.

Things that differ from the 3.x path: the helm repository URL change is a 3.x concern only, and the `mayastor.agents.core.rebuild.partial.enabled=false` option is not required for upgrades from 4.x to newer versions.

Keep in mind the page-wide rules. The 4.6 chart installs all four Local and Replicated engines regardless of what you used before, so add `--set engines.replicated.mayastor.enabled=false` if you only use Local PV. Downgrades are unsupported, so plan the upgrade as one-way. When deploying with the OpenEBS Helm chart, the `kubectl openebs upgrade` command upgrades all storages.

The page's see-also list points to the release notes and troubleshooting pages.

## Checked

Method: 2026-11-08 read the raw markdown of the cited upgrade page in full; steps match. Removed the unsupported 'one engine at a time' phrasing.
