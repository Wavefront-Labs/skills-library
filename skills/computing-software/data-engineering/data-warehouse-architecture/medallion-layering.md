---
id: computing-software.data-engineering.data-warehouse-architecture.medallion-layering
name: medallion-layering
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, medallion-architecture, bronze-silver-gold, raw-staging-marts, lakehouse, data-lake, data-warehouse, layering, staging-models, intermediate-models, data-marts, naming-conventions, access-control, unity-catalog, governance, dbt-project-structure, snowflake, databricks, bigquery, redshift, platform-selection]
level: practitioner
status: docs-checked
description: "Lay out a warehouse or lakehouse in layers: what belongs in bronze/silver/gold (raw/staging/marts), naming, access per layer, and platform criteria."
sources:
  - https://docs.databricks.com/aws/en/lakehouse/medallion
  - https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
  - https://docs.getdbt.com/best-practices/how-we-structure/2-staging
  - https://docs.getdbt.com/best-practices/how-we-structure/3-intermediate
  - https://docs.getdbt.com/best-practices/how-we-structure/4-marts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Medallion layering — where each piece of data belongs

**Goal:** every table has an obvious layer, an owner and a contract, so people know what they may build on, and raw history is never lost.

## 1. Two vocabularies, one idea
| Medallion (lakehouse) | dbt / warehouse | Purpose |
|---|---|---|
| Bronze | raw / sources (landing) | exact copy of what arrived |
| Silver | staging + intermediate | cleaned, typed, deduplicated, conformed |
| Gold | marts | business-ready facts, dimensions, metrics |
Pick one vocabulary per organization and use it in schema names, docs and tickets. The names matter less than the rules for each layer.

## 2. Bronze / raw — keep everything, change nothing
- Append-only, source-shaped, with ingestion metadata: `_loaded_at`, `_source_file` or `_kafka_offset`, `_batch_id`.
- Store semi-structured payloads as-is (JSON/VARIANT/STRING) when sources drift, so schema changes don't break ingestion.
- No business logic, no filtering except obvious garbage that can't be stored.
- Retain long enough to replay all downstream layers (often years; cheap object storage). This is your backfill insurance — see computing-software.data-engineering.etl-pipeline-design.idempotent-incremental-loads.
- **Gotcha:** PII lands here too. Restrict access tightly and plan deletion (GDPR erasure) requests here, not just in gold.

## 3. Silver / staging — one clean version of each source entity
- One staging model per source table. The dbt guide limits staging to renaming, type casting, basic computations (for example cents to dollars) and categorizing; it advises against joins and aggregations there, and materializes staging as views. In the Databricks medallion silver layer the work also includes schema enforcement, null handling, deduplication, late and out-of-order data, and quality checks. Put deduplication to the latest version per key, UTC normalisation, JSON parsing and soft-delete flags in whichever model your team designates, once, and document where.
- Databricks recommends building silver from bronze tables (mostly streaming reads), not writing to silver directly from ingestion, which couples it to source schema changes and corrupt records. Silver keeps at least one validated, non-aggregated representation of each record.
- Intermediate models prepare staging models for marts: re-graining (fan out or collapse), pivoting, and isolating complex logic; dbt suggests joining roughly 4 to 6 concepts per intermediate model so marts stay readable. They are not exposed to end users: default to ephemeral materialization, or views in a separate restricted schema. Still entity-centric, not report-centric.
- Apply data quality tests here (keys unique, not null, accepted values) — see computing-software.data-engineering.data-quality.data-tests-and-freshness-slas.
- Mask or tokenize PII where downstream doesn't need it.
- **Gotcha:** don't let silver become "bronze with renamed columns" — dedupe and typing belong here, or every gold model re-implements them differently.

## 4. Gold / marts — modelled for consumption
- Databricks gold is dimensional modelling plus aggregates (for example a materialized view such as weekly bookings) aligned to business functions; the dbt guide's marts are one wide, denormalised model per business entity at its grain (customers, orders), borrowing data from related concepts rather than rejoining at query time. If you use the dbt Semantic Layer, dbt advises staying more normalised. Pick star schemas with conformed dimensions (computing-software.data-engineering.data-modelling.dimensional-modelling-and-scd), entity marts or wide OBTs per consumer needs.
- Organized by business domain (`finance`, `marketing`), with an owner per mart and documented grain. Some organisations keep several gold layers (HR, finance, IT). Business-domain split starts after staging: the dbt guide advises against splitting staging by business group, because it breeds conflicting definitions of the same entity.
- Only gold is exposed to BI tools and broad analyst roles. Changes follow a contract/versioning process because dashboards depend on them.

## 5. Naming and structure
- Schemas: `bronze_<source>` / `silver` / `gold_<domain>`, or `raw_<source>` / `staging` / `marts_<domain>`. Databricks' example keeps each layer in a schema of one catalog (`ops.bronze`, `ops.silver`, `ops.gold`); you can also add catalogs per environment (`dev`, `prod`), e.g. `prod.silver.orders`.
- Model names (dbt guide): staging `stg_<source>__<entity>s` (double underscore between source and plural entity; a single-source project may drop the source), intermediate `int_<entity>s_<verb>s` (for example `int_order_items_summed_to_orders`), and marts named by the entity itself (`orders`, `customers`). The `fct_` / `dim_` prefixes are a common Kimball-style convention, not part of the dbt guide.
- One directory per layer in the transformation project mirrors the schemas.
- Lineage only flows forward: gold may read silver; silver may read bronze; nothing reads "up" and gold doesn't read bronze directly.

## 6. Access and governance per layer
| Layer | Who writes | Who reads |
|---|---|---|
| Bronze | ingestion service accounts only | data engineers, break-glass |
| Silver | transformation jobs | data engineers, analytics engineers |
| Gold | transformation jobs | analysts, BI service accounts, data apps |
Grant via roles or groups on schemas, never to individuals on tables (Snowflake grants privileges to roles, which are assigned to users; check your platform's equivalent). Tag PII columns and apply masking policies centrally.

## 7. Choosing the platform (criteria, not brand loyalty)
- **Workload mix:** SQL/BI-heavy versus heavy Spark/ML/streaming on open files.
- **Open formats:** need several engines on the same data, so consider open table formats (Iceberg, Delta).
- **Cost model:** how compute and storage are billed on each platform; model your real query mix from the vendor's pricing page.
- **Team skills,** existing cloud, governance features (lineage, masking, row filters), and data residency.
Layering works the same on any of them; Databricks calls the medallion pattern a recommended best practice, not a requirement.

## Checked
2026-11-08: Read in full: the Databricks medallion page and the dbt structure overview. Read the dbt staging, intermediate and marts pages for the relevant sections (naming, allowed transformations, materialization, denormalisation). The first 45 lines of the Snowflake access-control overview were read (roles hold privileges); the rest and the BigQuery introduction were not, so both sources and their claims (future grants, `GRANT SELECT ON SCHEMA`, dataset IAM, per-second and slot billing, named platform lists) were removed. Corrected: `fct_`/`dim_` are not dbt-guide prefixes; the dbt guide keeps staging free of joins and aggregations.
Method: documentation only; no commands were run.

## Verify
- [ ] Every table belongs to exactly one layer, visible from its schema name.
- [ ] Bronze is append-only and retains enough history to rebuild silver and gold.
- [ ] No gold model references a bronze table directly (check lineage graph).
- [ ] BI and analyst roles have no SELECT on bronze schemas.
- [ ] Each gold mart has a named owner and documented grain.
