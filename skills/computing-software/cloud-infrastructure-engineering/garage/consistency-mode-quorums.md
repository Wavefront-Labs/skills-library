---
id: computing-software.cloud-infrastructure-engineering.garage.consistency-mode-quorums
name: consistency-mode-quorums
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [consistency-mode, read-quorum, write-quorum, degraded-mode]
level: advanced
status: docs-checked
description: "Compare consistent, degraded and dangerous consistency_mode values and the read and write quorums each gives."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/reference-manual/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consistency_mode` (since v1.0.0) sets how reads and writes behave.

- `consistent` is the default. Quorums are chosen so read-after-write consistency holds.
- `degraded` lowers the read quorum to 1. You can read when several nodes or zones are unavailable, but read-after-write consistency is lost. The write quorum is unchanged.
- `dangerous` lowers both quorums to 1. It is the least consistent mode and the page says it should probably never be used.

Documented quorum table:

| mode | factor | write | read | read-after-write |
|---|---|---|---|---|
| consistent | 1 | 1 | 1 | yes |
| consistent | 2 | 2 | 1 | yes |
| dangerous | 2 | 1 | 1 | no |
| consistent | 3 | 2 | 2 | yes |
| degraded | 3 | 2 | 1 | no |
| dangerous | 3 | 1 | 1 | no |

Factor 2 with `degraded` behaves like `consistent`, since its read quorum is already 1. Factor 2 with `dangerous` writes the second replica asynchronously: a PutObject can return 200 OK before the second copy even starts, so a crash can lose data and new objects may not be visible at once. Its benefit is that writes still work with one node down.

Switching between modes while keeping `replication_factor` is easy: edit the config on all nodes and restart them.

## Checked

2026-11-04. Read the Configuration file format page in full. Confirmed the three modes, the six-row quorum table, the factor 2 examples and the mode-switching rule. Nothing removed.
Method: documentation only; no commands were run.
