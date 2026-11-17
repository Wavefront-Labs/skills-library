---
id: computing-software.data-engineering.dbt.seeds
name: seeds
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-seeds, seed-column-types, csv-seeds, reference-data, quote-columns, full-refresh-seeds, delimiter]
level: practitioner
status: verified
description: "Use dbt seeds for small static reference data: column_types, quoting, delimiter, full-refresh on schema change, testing seeds, and what should never be a seed."
sources:
  - https://docs.getdbt.com/docs/build/seeds
  - https://docs.getdbt.com/reference/seed-configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Seeds

**Goal:** version-control small, slowly changing lookup data (country codes, mapping tables, test fixtures) and load it with `dbt seed`.

## When to use
- Yes (docs give no numeric limit, only that seeds are not performant for large files): < a few thousand rows, changes via pull request, owned by the analytics team (channel mappings, account classifications, holiday calendars).
- No: raw business data, anything large (loads row-by-row inserts on some adapters; slow), data updated by business users (use a source loaded by a tool or a governed spreadsheet connector), secrets/PII (it lives in git).

## Configure types explicitly
```yaml
# dbt_project.yml
seeds:
  acme:
    +schema: reference
    country_codes:
      +column_types:
        iso2: varchar(2)
        numeric_code: varchar(3)       # keep leading zeros: inference would make it int
        eu_member: boolean
      +quote_columns: false
      +delimiter: ","                  # 1.7+: e.g. ";" or "|"
```
Type inference guesses from values: `007` was loaded as integer 7 on dbt-duckdb (checked), and mixed date formats become text. Always pin types for identifier-like columns; the target type must be valid on your warehouse (DuckDB ignores the `varchar(2)` length).

## Load
```bash
dbt seed                         # truncates the existing table and re-inserts (no drop cascade)
dbt seed --full-refresh          # drop and recreate: required after column changes
dbt seed -s country_codes
```
`dbt build` includes seeds in DAG order. Reference with `{{ ref('country_codes') }}`.

## Test them
```yaml
seeds:
  - name: country_codes
    columns:
      - name: iso2
        data_tests: [unique, not_null]
```

## Gotchas
- Adding or renaming columns without `--full-refresh` fails (on dbt-duckdb the CSV sniffer error appeared; the docs show Snowflake and Redshift column-not-found errors). `--full-refresh` drops with cascade, which can drop downstream objects BI tools query.
- `dbt seed --empty` replaced an existing seed table with zero rows on dbt 1.12.6 (checked).
- Large CSV diffs in PRs are hard to review; keep seeds narrow and sorted.
- Encoding: save as UTF-8. dbt's CSV loader strips a leading BOM (dbt-common `from_csv`; a BOM file loaded with a clean first column name on dbt 1.12.6), so no BOM clean-up is needed.

## Verify
- [ ] `dbt seed` + tests pass in CI.
- [ ] Column types in the warehouse match `column_types`.
