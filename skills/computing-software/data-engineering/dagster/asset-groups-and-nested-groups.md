---
id: computing-software.data-engineering.dagster.asset-groups-and-nested-groups
name: asset-groups-and-nested-groups
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, groups, group-name, nested-groups, asset-graph, organization]
level: practitioner
status: docs-checked
description: "Assign Dagster assets to a single group with group_name, nest groups with / separators, and see how groups render in the asset graph."
sources:
  - https://docs.dagster.io/guides/build/assets/metadata-and-tags/groups
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Asset groups

Goal: organize assets into boxes in the asset graph.

- Assets are in the `default` group unless you set `group_name`.
- `group_name` is accepted wherever assets are defined or modified: `AssetSpec`, the `group_name` argument to `load_assets_from_modules`, attributes of a `defs.yaml` file, and integration translators such as the dbt translator `get_group_name`.
- An asset has only one group. For several dimensions at once use tags.
- Nested groups: use `/` in the name (`marketing/paid`). Parent groups are implied by children, so `marketing` need not be declared. Requires Dagster 1.13.9 or later.
- Selection: `group:"team1"` matches the exact name; `group:"team1/*"` matches nested groups under team1 but not team1 itself.
- UI: each group is a labeled box, nested groups are boxes inside the parent. Clicking a group header collapses it into one node with rolled-up status counts, clicking again expands. The sidebar shows the same hierarchy as a tree.

## Checked

2026-11-03. Pages read in full against this skill:
- https://docs.dagster.io/guides/build/assets/metadata-and-tags/groups

Confirmed: the identifiers, settings, defaults, numbers and behaviours stated above, against the page text and its code examples.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
