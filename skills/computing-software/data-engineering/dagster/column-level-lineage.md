---
id: computing-software.data-engineering.dagster.column-level-lineage
name: column-level-lineage
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, column-lineage, tablecolumnlineage, tablecolumndep, deps-by-column, metadata]
level: advanced
status: docs-checked
description: "Emit dagster/column_lineage with TableColumnLineage and TableColumnDep from MaterializeResult; viewing in the UI needs Dagster+."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/column-level-lineage
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Column-level lineage

Goal: show how each column of a table asset derives from columns in other assets.

## Emit it
1. Return a `MaterializeResult` with a `metadata` parameter.
2. Use the key `dagster/column_lineage` with a `TableColumnLineage` object.
3. Build it with `TableColumnLineage.deps_by_column`, mapping each column to its dependencies.
4. Each dependency is a `TableColumnDep(asset_key=..., column_name=...)`.

Docs example: `my_asset` creates `new_column_foo` (depends on `column_bar` of `source_bar` and `column_baz` of `source_baz`) and `new_column_qux` (depends on `column_quuz` of `source_bar`).

## Integrations
Supported for the dbt integration.

## View it
Viewing is a Dagster+ feature. Open **Asset details**, the **Overview** tab, and in the **Columns** section click the branch icon at the far right of the column row. Use the **Column** dropdown to switch columns.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/metadata-and-tags/column-level-lineage

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
