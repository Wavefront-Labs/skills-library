---
id: computing-software.data-engineering.dagster.asset-selection-filters-and-layers
name: asset-selection-filters-and-layers
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, asset-selection, key-filter, tag, owner, group, kind, upstream-downstream]
level: practitioner
status: docs-checked
description: "Write Dagster asset selection queries: key, tag, owner, group, kind filters, +/N+ layer traversal, and/or/not, roots() and sinks()."
sources:
  - https://docs.dagster.io/guides/build/assets/asset-selection-syntax/reference
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset selection syntax

Goal: write selection strings for jobs, UI and CLI.

## Filters
- `key:"my_asset"`, wildcard `key:"prefix_*"`, multiple `key:"prefix_*_middlefix_*_suffix"`
- `tag:"stage"` or `tag:"stage"="value"`
- `owner:"alice"`, `group:"team1"` (exact, including `/` separators), `group:"team1/*"` (nested groups under team1, not team1 itself)
- `kind:"table"`, `code_location:"repo1"`
- Dagster+ only: `column_tag`, `columns`, `table_name`, `status: "DEGRADED"` (HEALTHY, WARNING, DEGRADED, UNKNOWN, NOT_APPLICABLE)
- Dagster+ branch deployments only: `changed_in_branch: "ANY"` (or CODE_VERSION, DEPENDENCIES, METADATA, NEW, PARTITIONS_DEFINITION, TAGS)

Only `key` and `group` support wildcards, and a selection containing `*` must be quoted.

## Layers
- `+key:"x"` all upstream, `1+key:"x"` one layer up, `2+key:"x"` two up
- `key:"x"+`, `key:"x"+1`, `key:"x"+2` downstream equivalents
- `1+key:"x"+1` or `+key:"x"+` both directions

## Combining
`and`, `or`, `not`, and parentheses: `(owner:"alice" or group:"analytics") and kind:"table"`.

## Functions
`roots(selection)` (no upstream within the selection) and `sinks(selection)`. Examples: `roots(*)`, `sinks(group:"public_data")`, `roots(+group:"public_data")`.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/asset-selection-syntax/reference

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
