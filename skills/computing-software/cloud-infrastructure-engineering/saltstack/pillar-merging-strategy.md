---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-merging-strategy
name: pillar-merging-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, merging, pillar-source-merging-strategy, pillar-merge-lists, namespace]
level: advanced
status: docs-checked
description: "Control how Salt merges overlapping pillar keys: last-wins flattening, pillar_source_merging_strategy values, pillar_merge_lists and include override."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/pillar/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pillar merging

Namespace flattening: files listed later overwrite conflicting top-level keys ("last one wins"). Nest keys under a parent name to avoid collisions.

Master options:
- `pillar_source_merging_strategy`: `smart` (default), `recurse`, `aggregate`, `overwrite`, or `none`. `smart` chooses `recurse` unless the renderer pipeline ends in `yamlex`, which selects `aggregate`.
- `pillar_merge_lists`: `False` (default) replaces lists; `True` appends the later list.
- `pillar_includes_override_sls`: by default includes merge first and the including SLS wins; `True` restores the pre-2017.7.3 layering.

Grain merging is separate: the minion config overrides grains from grain modules, and the pillar strategies do not apply.

## Checked

2026-11-04: read the Salt pillar reference page in full. Confirmed last-wins flattening, the five pillar_source_merging_strategy values and smart behaviour, pillar_merge_lists, pillar_includes_override_sls (2017.7.3) and grain merging. Nothing removed.

Method: documentation only; no commands were run.

