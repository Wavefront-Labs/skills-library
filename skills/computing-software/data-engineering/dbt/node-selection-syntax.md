---
id: computing-software.data-engineering.dbt.node-selection-syntax
name: node-selection-syntax
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, node-selection, selectors-yml, graph-operators, select-exclude, tag-selector, path-selector, indirect-selection, dbt-ls]
level: practitioner
status: verified
description: "Select exactly the dbt nodes you mean: graph operators (+, n+, @), tag/path/source/config methods, unions and intersections, --exclude, selectors.yml, indirect selection."
sources:
  - https://docs.getdbt.com/reference/node-selection/syntax
  - https://docs.getdbt.com/reference/node-selection/methods
  - https://docs.getdbt.com/reference/node-selection/yaml-selectors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node selection syntax

**Goal:** run, test or list precisely the part of the DAG you intend, and name common selections.

## Building blocks
```bash
dbt build -s fct_orders                 # one node
dbt build -s +fct_orders                # it and all ancestors
dbt build -s fct_orders+                # it and all descendants
dbt build -s 2+fct_orders+1             # 2 levels up, 1 down
dbt build -s @stg_orders                # descendants plus all their ancestors (safe "rebuild everything affected")
dbt build -s tag:nightly
dbt build -s path:models/marts/finance
dbt build -s source:stripe+
dbt build -s config.materialized:incremental
dbt build -s resource_type:snapshot     # or --resource-type snapshot
dbt build -s "package:dbt_artifacts"
dbt build -s "fct_*"                    # wildcard on names
```
- Space-separated = **union**: `-s tag:finance tag:marketing`.
- Comma = **intersection**: `-s tag:nightly,config.materialized:table`.
- `--exclude` removes: `dbt build -s marts --exclude tag:deprecated`.

## Always preview
```bash
dbt ls -s "tag:nightly,+fct_orders" --resource-type model
```

## selectors.yml
```yaml
selectors:
  - name: nightly_finance
    description: finance marts and everything they need, minus heavy backfill models
    definition:
      union:
        - intersection:
            - method: tag
              value: finance
            - method: path
              value: models/marts
              parents: true
        - exclude:
            - method: tag
              value: backfill_only
```
`dbt build --selector nightly_finance`. Named selectors keep orchestration code free of fragile strings and are reviewable.

## Tests and indirect selection
When you select a model, tests on it run too (`--indirect-selection eager` default: any test touching a selected node, including relationships tests to unselected parents). `cautious` runs only tests whose parents are all selected; `buildable` runs tests whose parents are each selected or an ancestor of the selection (slightly more inclusive); `empty` runs no tests. With `-s fct_orders` and a relationships test to `stg_customers` (not selected, but upstream): eager 4 tests, cautious 3, buildable 4. Use `cautious` in CI on partial DAGs to avoid tests failing due to unbuilt parents (dbt reference: indirect selection).

## Verify
- [ ] `dbt ls` output for each orchestration selector is reviewed in the PR that changes it.
- [ ] No orchestration job uses an unbounded selector by accident (e.g. missing `+` meaning parents never rebuild).
