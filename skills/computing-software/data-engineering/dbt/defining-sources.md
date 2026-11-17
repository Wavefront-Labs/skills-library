---
id: computing-software.data-engineering.dbt.defining-sources
name: defining-sources
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-sources, source-function, sources-yml, identifier, quoting, source-tests, source-freshness, lineage]
level: practitioner
status: docs-checked
description: "Declare raw tables as dbt sources: sources YAML with database/schema/identifier, source() vs hard-coded names, tests and freshness on sources, and one staging model per source."
sources:
  - https://docs.getdbt.com/docs/build/sources
  - https://docs.getdbt.com/reference/source-properties
  - https://docs.getdbt.com/reference/commands/source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining sources

**Goal:** every raw table the project reads is declared once, so lineage starts at the true source, environments can repoint it, and quality checks attach to it.

## YAML
```yaml
# models/staging/stripe/_stripe__sources.yml
sources:
  - name: stripe
    database: raw
    schema: stripe
    loader: fivetran
    config:
      loaded_at_field: _fivetran_synced   # under config from v1.10
      freshness:                          # under config from v1.9
        warn_after: {count: 6, period: hour}
        error_after: {count: 24, period: hour}
    tables:
      - name: charges
        identifier: CHARGES_V2            # physical name if different
        description: "One row per Stripe charge"
        columns:
          - name: id
            data_tests: [unique, not_null]
      - name: customers
        config:
          freshness: null                 # opt out for slowly changing tables
```

## Use source(), never raw names
```sql
-- models/staging/stripe/stg_stripe__charges.sql
select id as charge_id, amount / 100.0 as amount, currency, created as created_at
from {{ source('stripe', 'charges') }}
```
Using `source()` creates a dependency between the model and the source table and defines lineage; hard-coded names do not.

## Conventions
- Only models should select from a source through `source()`; the best-practice layout is one staging model per source table (`stg_<source>__<table>`).
- Source properties can live in any properties `.yml` file under `models/`.
- `quoting` (database, schema, identifier: true or false) can be set on a source or table for names that need quoting.
- Declare `data_tests` on source columns to test assumptions about source data.

## Useful commands
```bash
dbt source freshness                          # writes target/sources.json (change with --output)
dbt build -s source:stripe+                   # everything downstream of stripe
dbt ls --resource-type source
```

## Verify
- [ ] Every model reads raw tables through `source()`, not hard-coded names.
- [ ] The docs lineage graph starts at sources for every staging model.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt sources and source-properties docs: source/table properties (`database`, `schema`, `loader`, `identifier`, `quoting`, `data_tests`), `freshness` with `warn_after`/`error_after` count and period and `loaded_at_field` now under `config` (v1.9/v1.10), `freshness: null` opt-out, `source()` creating lineage, `source:` selection, `dbt source freshness` writing `target/sources.json` with `--output`. Removed the env_var database example and unconfirmed claims about Snowflake case issues and `grep` verification.

Method: documentation only; no commands were run.
