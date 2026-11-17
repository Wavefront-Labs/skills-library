---
id: computing-software.data-engineering.dbt.model-yaml-file-layout
name: model-yaml-file-layout
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, model-yaml-layout, project-structure, schema-yml, properties-files]
level: practitioner
status: docs-checked
description: "Lay out dbt YAML property files per folder (_models.yml, _sources.yml, _docs.md) so docs, tests and sources stay findable, reviewable and conflict-free."
sources:
  - https://docs.getdbt.com/best-practices/how-we-structure/2-staging
  - https://docs.getdbt.com/reference/configs-and-properties
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model YAML file layout

**Goal:** a predictable place for every model's description, tests and config, with small diffs and few merge conflicts.

## Convention (dbt Labs staging guide)
The current staging page shows one YAML file per model next to its SQL, plus a sources file:
```
models/staging/
  __sources.yml
  stg_customers.sql
  stg_customers.yml
  stg_orders.sql
  stg_orders.yml
```
- Alternative many teams use: one `_models.yml` per folder with a block per model, and a leading underscore so it sorts first. Pick one convention and enforce it.

## Avoid
- A single giant `schema.yml` at the root: constant merge conflicts, slow review.
- The same model described in two files.
- Configs split between `dbt_project.yml`, YAML and `config()` for no reason: folder-level defaults in `dbt_project.yml`, exceptions in YAML or the model.

## Skeleton
```yaml
version: 2
models:
  - name: stg_stripe__payments
    description: "{{ doc('stripe_payments') }}"
    columns:
      - name: payment_id
        data_tests: [unique, not_null]
```
`data_tests:` is the key used in the dbt docs; check your dbt version's docs for the older `tests:`.

## Tooling
- `dbt-project-evaluator` runs checks over a dbt project and can help enforce conventions.

## Verify
`dbt parse` succeeds with no duplicate-description errors; every model has a YAML entry in your chosen layout.

## Checked

2026-10-28. Confirmed against: staging structure page (per-model YAML, __sources.yml), configs-and-properties and meta pages (data_tests key), dbt-project-evaluator README. Removed (not confirmable in the fetched pages): _stripe__models.yml convention (current guide shows per-model YAML), 1.8 gate, codegen and osmosis commands, duplicate patch error text.

Method: documentation only; no commands were run.
