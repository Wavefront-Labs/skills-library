---
id: computing-software.data-engineering.data-modelling.data-vault-with-automate-dv
name: data-vault-with-automate-dv
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, data-vault, automate-dv, dbt, hub, link, satellite, hashdiff, staging, pit-table]
level: practitioner
status: docs-checked
description: "Generate Data Vault 2.0 hubs, links and satellites with the AutomateDV dbt package: staging with hash keys and hashdiffs, macro configs, incremental loads, PITs and bridges."
sources:
  - https://automate-dv.readthedocs.io/en/latest/
  - https://automate-dv.readthedocs.io/en/latest/macros/
  - https://automate-dv.readthedocs.io/en/latest/tutorial/tut_staging/
  - https://hub.getdbt.com/Datavault-UK/automate_dv/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Vault with AutomateDV (dbt)

**Goal:** build a raw vault from metadata in dbt, with consistent hashing and insert-only incremental loads, instead of hand-writing hundreds of near-identical models.

## 1. Install
```yaml
# packages.yml
packages:
  - package: Datavault-UK/automate_dv
    version: [">=0.11.0", "<0.12.0"]       # pin a range; check hub for current
```
```yaml
# dbt_project.yml — global hashing settings (decide once, never change)
vars:
  hash: MD5                   # or SHA
  concat_string: '||'
  null_placeholder_string: '^^'
  hash_content_casing: UPPER  # applied before hashing
```

## 2. Staging: hash keys and hashdiffs
```sql
-- models/staging/v_stg_orders.sql
{%- set yaml_metadata -%}
source_model: {raw_shop: orders}
derived_columns:
  RECORD_SOURCE: "!SHOP.ORDERS"
  LOAD_DATETIME: "_loaded_at"
  EFFECTIVE_FROM: "updated_at"
hashed_columns:
  CUSTOMER_HK: customer_id
  ORDER_HK: order_id
  CUSTOMER_ORDER_HK: [customer_id, order_id]
  ORDER_HASHDIFF:
    is_hashdiff: true
    columns: [status, amount, currency]
{%- endset -%}
{% set metadata_dict = fromyaml(yaml_metadata) %}
{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     hashed_columns=metadata_dict['hashed_columns']) }}
```
`!` prefix = string constant. Business keys are trimmed/upper-cased per settings before hashing — do key cleansing here, consistently.

## 3. Raw vault models
```sql
-- hub_customer.sql
{{ config(materialized='incremental') }}
{{ automate_dv.hub(src_pk='CUSTOMER_HK', src_nk='customer_id', src_ldts='LOAD_DATETIME',
                   src_source='RECORD_SOURCE', source_model='v_stg_orders') }}
-- link_customer_order.sql
{{ config(materialized='incremental') }}
{{ automate_dv.link(src_pk='CUSTOMER_ORDER_HK', src_fk=['CUSTOMER_HK','ORDER_HK'], src_ldts='LOAD_DATETIME',
                    src_source='RECORD_SOURCE', source_model='v_stg_orders') }}
-- sat_order_details.sql
{{ config(materialized='incremental') }}
{{ automate_dv.sat(src_pk='ORDER_HK', src_hashdiff='ORDER_HASHDIFF', src_payload=['status','amount','currency'],
                   src_eff='EFFECTIVE_FROM', src_ldts='LOAD_DATETIME', src_source='RECORD_SOURCE',
                   source_model='v_stg_orders') }}
```
- Hubs/links insert only new keys; satellites insert only when the hashdiff changes vs the latest row per key.
- Multiple sources into one hub: `source_model=['v_stg_orders', 'v_stg_crm_customers']`.
- Other macros: `t_link` (transactions), `eff_sat` (effectivity), `ma_sat` (multi-active), `xts`. `pit` and `bridge` exist but are deprecated since AutomateDV v0.11.0 (the docs call them not fit-for-purpose pending a redesign); check the macros page before relying on them.

## 4. Query layer
- PIT tables snapshot, per hub key and as-of date, which satellite row was valid, which makes point-in-time joins equi-joins. The `automate_dv.pit` macro is deprecated since v0.11.0; build PITs in your own model if you need them.
- Build business vault and information marts (star schemas) on top; don't expose raw vault to BI.

## 5. Gotchas
- Changing hash algorithm, casing or concat string later invalidates every key — fix in project vars before the first load.
- The hashdiff column list must include all payload columns; adding a column changes hashdiffs → one new satellite row per key on the next load. Plan it.
- Satellites need deduplicated staging per key per load (multiple changes per batch: ensure one row per key per `LOAD_DATETIME`, or load in ordered batches). The satellite `apply_source_filter` config (added v0.10.1) is different: it only skips source rows with `src_ldts` at or before the satellite's current max load date.
- The docs let you choose MD5 or SHA-256 hashing (`hash` var); decide once.

## Verify
- [ ] Re-running the same batch inserts 0 rows in hubs, links and satellites.
- [ ] A changed payload inserts exactly one satellite row for that key.
- [ ] Hash settings are pinned in `dbt_project.yml` vars.

## Checked

2026-11-02. Confirmed against the AutomateDV docs (home, macros, staging tutorial) and the dbt Hub page: global vars `hash`, `concat_string`, `null_placeholder_string`, `hash_content_casing` and their example values; `stage` macro and `include_source_columns`; `hub`/`link`/`sat`/`t_link`/`eff_sat`/`ma_sat`/`xts` macro names and parameters (`src_eff`, `src_hashdiff`); the `!` constant prefix; MD5 and SHA-256 options; hub latest version 0.11.5, so the `>=0.11.0,<0.12.0` range is valid. Fixed: `pit` and `bridge` are deprecated since v0.11.0; `apply_source_filter` is not a per-key dedupe. Removed: the unsourced claim that hashdiff column order matters and the MD5-collision remark.

Method: documentation only; no commands were run.
