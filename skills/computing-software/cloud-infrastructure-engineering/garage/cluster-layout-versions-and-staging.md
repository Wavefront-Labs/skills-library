---
id: computing-software.cloud-infrastructure-engineering.garage.cluster-layout-versions-and-staging
name: cluster-layout-versions-and-staging
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [cluster-layout, layout-show, layout-revert, staged-changes]
level: practitioner
status: docs-checked
description: "Understand how Garage layouts are versioned, staged with assign and remove, and applied or reverted."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/known-issues/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The cluster layout is a table giving each node a role: a storage node with a capacity, or a gateway node that stores no data. Data is divided into partitions, and the layout maps partitions to nodes. It has three parts: the user-defined role table, an optimal partition assignment computed once when you run `garage layout apply` (or the ApplyClusterLayout API call), and a version number. Nodes always use the highest version.

Nodes also share a set of proposed, not yet applied role changes. Commands that stage changes for the next version:

- `garage layout assign [...]`
- `garage layout remove [...]`

Inspect the current layout and proposals with `garage layout show`. Then either create the next version including the changes, or cancel them:

- `garage layout apply --version <new_version_number>`
- `garage layout revert --version <new_version_number>`

The new version number must be exactly the previous version plus one, or both commands fail. The same operations exist in the admin API with very similar semantics.

If the layout stays stuck with several active versions after nodes were swapped, the known-issues page says `garage layout history` diagnoses it and prints instructions. The `-t` tag option must be repeated per tag, since comma-separated values become one string.

## Checked

2026-11-04. Read the Cluster layout management and Known issues pages in full. Confirmed the three layout components, the staging commands, show, apply and revert with the plus-one version rule, the admin API remark, the layout history diagnosis and the -t tag note. Nothing removed.
Method: documentation only; no commands were run.
