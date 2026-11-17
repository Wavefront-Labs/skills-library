---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.modify-filter-rules
name: modify-filter-rules
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, modify-filter, rename, set-add, remove, record-editing]
level: practitioner
status: docs-checked
description: "Add, set, rename, copy, remove and reorder record keys with the modify filter's rules."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/modify"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Modify filter rules

The `modify` filter changes records with rules, applied in order, each acting on the result of the previous one. Any number of rules can be set in one instance. Rule names are case-insensitive; parameters are not.

| Rule | Effect |
| --- | --- |
| `Set KEY VALUE` | add the pair; overwrite if `KEY` exists |
| `Add KEY VALUE` | add the pair only if `KEY` does not exist |
| `Remove KEY` | remove `KEY` if present |
| `Remove_wildcard KEY` | remove all keys matching the wildcard |
| `Remove_regex KEY` | remove all keys matching the regular expression |
| `Rename KEY NEW` | rename if `KEY` exists and `NEW` does not |
| `Hard_rename KEY NEW` | rename if `KEY` exists, overwriting `NEW` |
| `Copy KEY NEW` | copy if `KEY` exists and `NEW` does not |
| `Hard_copy KEY NEW` | copy if `KEY` exists, overwriting `NEW` |
| `Move_to_start KEY` | move keys matching the wildcard to the start |
| `Move_to_end KEY` | move keys matching the wildcard to the end |

Example intent: rename `Key2` to `RenamedKey` and add `OtherKey` with `Value3` when it is missing.

```yaml
pipeline:
  filters:
    - name: modify
      match: '*'
      Rename: Key2 RenamedKey
      Add: OtherKey Value3
```

`Rename` and `Copy` do nothing when the target exists; choose the `Hard_` forms to overwrite. Place `Remove` after any `Copy` that needs the source key.


## Checked

2026-11-03. Confirmed on the Fluent Bit Modify filter page: all eleven rules and their semantics, case-insensitive rule names, ordering, and the rename and add example. Removed: an unsourced verification step.

Method: documentation only; no commands were run.
