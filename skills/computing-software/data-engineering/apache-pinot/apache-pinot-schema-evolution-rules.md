---
id: computing-software.data-engineering.apache-pinot.apache-pinot-schema-evolution-rules
name: apache-pinot-schema-evolution-rules
category: computing-software
field: data-engineering
product: apache-pinot
tags: [apache-pinot, schema-evolution, reload, forcecommit, consuming-segment, transformconfigs, erroroncolumnbuildfailure, additive-changes]
level: advanced
status: docs-checked
description: "Pinot schema changes: additive only, rename/drop/type change need a new table, reload and consuming segments, chained derived columns."
sources: ["https://github.com/pinot-contrib/pinot-docs/blob/latest/build-with-pinot/data-modeling/schema-evolution.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema evolution rules

Schema changes are **additive**: you may add columns. Renames, drops and data type changes are table redesign work: create a new table instead.

After uploading the changed schema, completed segments must be **reloaded** to materialise the new column. When `pinot.server.instance.reload.consumingSegment` is true (the default), reloading a consuming segment requests a force commit; it seals asynchronously and a replacement consumer starts on the latest schema. Reload completion is not a barrier that the new consumers are online: call `POST /tables/{tableName}/forceCommit` and poll its status for that.

Derived columns defined in `ingestionConfig.transformConfigs` are computed on reload and can depend on each other (chained). Dependencies are evaluated before dependents regardless of listing order. Cycles are not supported: every cycle member falls back to its default value with a warning, and `errorOnColumnBuildFailure` does not turn that fallback into a failure, so break the cycle in the config.

Things that need a pause boundary or a new table:
- changing an existing transform function,
- changing immutable upsert settings (primary key, comparison columns),
- partial-upsert tables, where you verify the Helix cluster config `pinot.server.consuming.segment.consistency.mode` before a pause, force commit or reload of consuming segments.

For a plain additive column the page's flow is: add the column (with a `defaultNullValue` if older rows should show a default), update the table or ingestion config if needed, make consuming segments pick up the new schema (reload or forceCommit), then reload completed segments.

## Checked

2026-11-09: confirmed against the Pinot Schema evolution page (pinot-docs build-with-pinot/data-modeling/schema-evolution.md): additive-only rule, rename/drop/type change as table redesign, the typical flow, `pinot.server.instance.reload.consumingSegment` default and force commit behaviour, the decision table rows for transforms, full and partial upsert and the immutable upsert settings, and chained derived columns with cycle fallback. Corrected the claim that `errorOnColumnBuildFailure` fails a cycle (the page says it does not) and removed the unconfirmed safe-order sentence.

Method: documentation only; no commands were run.
