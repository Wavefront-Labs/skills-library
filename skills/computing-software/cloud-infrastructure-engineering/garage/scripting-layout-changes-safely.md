---
id: computing-software.cloud-infrastructure-engineering.garage.scripting-layout-changes-safely
name: scripting-layout-changes-safely
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [layout-apply-version, scripted-layout, same-rpc-host, layout-consistency]
level: advanced
status: docs-checked
description: "Avoid inconsistent clusters when scripting layout changes: one host, one apply, strictly after staging."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/layout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The layout page opens its warnings with a hard rule: never call `garage layout apply` or `garage layout revert` several times with the same `--version`. Doing so can create several different layouts with the same version number, and the cluster becomes inconsistent until fixed. If a call failed and `garage layout show` shows the new version was not set, repeating the same version is fine.

Typing commands by hand is low risk if you run them one at a time and read `garage layout show` before applying.

When scripting through the CLI or admin API, the recommendations are:

- Send all CLI calls to the same RPC host; with the API, send all calls to the same Garage node. Do not split staged changes across nodes, since changes propagate asynchronously and some may be missing when the layout is applied.
- Call `garage layout apply` (ApplyClusterLayout) only once.
- Call it strictly after every `garage layout assign` and `garage layout remove` (UpdateClusterLayout) call has returned.

Pair this with version arithmetic: read the current version from `garage layout show` and apply version plus one.

## Checked

2026-11-07. Read in full (stripped page text, including the inline code blocks; no linked include files were opened): Cluster layout management. Confirmed on the layout page: the never-repeat-`--version` rule and the exception after a failed call, the same-host and single-apply recommendations, the ordering rule, and that the new version is 1 plus the previous one. No changes needed.

Method: documentation only; no commands were run.
