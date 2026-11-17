---
id: computing-software.data-engineering.dbt.model-deprecation-and-breaking-changes
name: model-deprecation-and-breaking-changes
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-mesh, deprecation-date, model-versions, breaking-change-detection, dbt-contracts, latest-version, state-modified]
level: advanced
status: docs-checked
description: "Retire and change dbt models safely: deprecation_date warnings, versioned models with latest_version, contract-based breaking-change detection in CI, and migration windows."
sources:
  - https://docs.getdbt.com/reference/resource-properties/deprecation_date
  - https://docs.getdbt.com/docs/mesh/govern/model-versions
  - https://docs.getdbt.com/reference/resource-configs/contract
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Model deprecation and breaking changes

**Goal:** consumers get warned before a model changes shape or disappears, and contracts catch accidental breaking changes.

## Breaking-change detection
With an enforced contract, dbt checks that the model's returned dataset matches the YAML-defined `name` and `data_type` of every column, and errors if not:
```yaml
models:
  - name: dim_customers
    access: public
    config:
      contract: {enforced: true}
    columns:
      - {name: customer_id, data_type: varchar, constraints: [{type: not_null}]}
      - {name: segment, data_type: varchar}
```
Removing or renaming a column, or changing its data type, is a breaking change for a contracted model; make it intentionally only by creating a new model version. Adding a column or fixing a bug in a column's calculation is non-breaking and needs no new version.

## Versioning a breaking change
```yaml
models:
  - name: dim_customers
    latest_version: 1
    config: {contract: {enforced: true}}
    columns: [...]
    versions:
      - v: 1
      - v: 2
        columns:
          - include: all
            exclude: [segment]          # v2 drops segment
          - {name: customer_tier, data_type: varchar}
        # defined_in: dim_customers_v2   (default file name)
```
- `ref('dim_customers')` resolves to `latest_version` (1) until you bump it; consumers opt in with `ref('dim_customers', v=2)`.
- The default file name for a version is `<model>_v<version>` (for example `dim_customers_v2.sql`); the latest version can live in a file without a suffix.
- For a stable name, dbt has a `latest_version_pointer` model config (project default via the `latest_version_pointer_enabled_by_default` flag, optional `alias`).

## Deprecate the old version
```yaml
      - v: 1
        deprecation_date: 2026-12-31
```
dbt warns with `DeprecatedModel` when parsing a project that defines a deprecated model, `DeprecatedReference` when a model past its date is referenced, and `UpcomingReferenceDeprecation` for a future date; `WARN_ERROR_OPTIONS` can promote these to errors. The date uses RFC 3339 formats (`YYYY-MM-DD` works); without an offset it is read in the system time zone of the dbt environment. dbt does not drop relations for deprecated models, and with an enforced contract you cannot delete the model before its `deprecation_date`.

## Migration window procedure
1. Ship v2 alongside v1 (latest_version still 1). Announce with dates.
2. Track consumers: exposures, cross-project refs (dbt Explorer), warehouse access history.
3. Bump `latest_version: 2` once major consumers moved.
4. Set `deprecation_date` on v1; remove v1 after the date and after access history shows no reads.

## Gotchas
- Changing only SQL logic (same columns/types) passes the contract but can still break semantics; use unit tests and data diffs.
- For contracted incremental models use `on_schema_change` of `append_new_columns` (or `fail`), not `sync_all_columns`, which removes deleted columns.

## Verify
- [ ] A change that drops a column from a contracted model fails the build.
- [ ] Downstream builds show deprecation warnings for v1 refs.

## Checked

2026-10-31. Confirmed against the dbt docs pages for `deprecation_date`, model versions and `contract`: warning names and scenarios, `WARN_ERROR_OPTIONS`, date formats and time zone rule, no relation dropping, no deletion of contracted models before the date, default `_v<version>` file naming, `ref` resolving to the latest version, `latest_version_pointer`, contract column checks and the `append_new_columns` advice. Removed: `state:modified` detection, `ContractBreakingChangeError`, post-hook macro advice, manifest and private-model gotchas.

Method: documentation only; no commands were run.
