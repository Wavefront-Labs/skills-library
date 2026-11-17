---
id: computing-software.data-engineering.dagster.definition-and-runtime-metadata
name: definition-and-runtime-metadata
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, metadata, materializeresult, metadatavalue, definition-metadata, runtime-metadata]
level: practitioner
status: docs-checked
description: "Attach definition-time and runtime (MaterializeResult) metadata to Dagster assets and use standard dagster/ metadata keys."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/index
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Definition and runtime metadata

Goal: attach rich info (Markdown description, table schema, row counts) to assets.

## Definition metadata
Set at code load time, identical for every materialization until code changes. Available inside I/O managers: in `handle_output` use `context.definition_metadata`; in `load_input` the upstream asset metadata is `context.upstream_output.definition_metadata` (`context.definition_metadata` there refers only to metadata declared on the downstream `AssetIn`/`In`).

## Runtime metadata
Return a `MaterializeResult` with a `metadata` dict (string keys). Wrap values in `MetadataValue` or use primitive Python types, which Dagster converts. Numeric metadata renders as a time series in the UI.

Warning: runtime metadata goes to the event log, not the I/O manager, so it is not available from `InputContext`. An I/O manager cannot persist it and read it back for downstream assets.

## Special keys in the UI
`dagster/uri` (str), `dagster/column_schema` (TableSchema), `dagster/column_lineage` (TableColumnLineage), `dagster/row_count` (int), `dagster/partition_row_count` (int), `dagster/table_name` (fully qualified str), `dagster/code_references` (definition-level only, not materialization metadata).

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/metadata-and-tags/index

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
