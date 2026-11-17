---
id: computing-software.data-engineering.dbt.docs-generate-and-persist-docs
name: docs-generate-and-persist-docs
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-docs, persist-docs, doc-blocks, dbt-docs-generate, dbt-docs-serve, column-descriptions, static-docs-site, dbt-docs-hosting]
level: practitioner
status: docs-checked
description: "Document a dbt project: descriptions in YAML, reusable {% docs %} blocks, persist_docs to push comments into the warehouse, and generating the docs site."
sources:
  - https://docs.getdbt.com/docs/build/documentation
  - https://docs.getdbt.com/reference/resource-configs/persist_docs
  - https://docs.getdbt.com/reference/commands/cmd-docs
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Docs: generate, doc blocks, persist_docs

**Goal:** descriptions written once in the project show up in the docs site, in the warehouse's own catalog, and in BI tools reading column comments.

## Write descriptions
```yaml
models:
  - name: fct_orders
    description: "{{ doc('fct_orders') }}"
    columns:
      - name: order_id
        description: Primary key. One row per order placed on web or app.
      - name: net_amount
        description: "{{ doc('net_amount') }}"
```
```markdown
<!-- models/docs/finance.md -->
{% docs net_amount %}
Order amount after discounts and before tax, in the order currency. Refunds are not deducted (see fct_refunds).
{% enddocs %}
```
Doc blocks keep long or shared definitions consistent; a docs block named `__overview__` replaces the docs site landing page. Docs blocks live in `.md` files found in the project resource paths.

## Push into the warehouse
```yaml
# dbt_project.yml
models:
  +persist_docs: {relation: true, columns: true}
```
dbt writes table and column comments to the database after building. `persist_docs` is supported on Postgres, Redshift, Snowflake, BigQuery, Databricks, Apache Spark and Starburst Galaxy (`dbt-trino`), not implemented for sources, and some databases limit where descriptions can be added. Known limits: Databricks column comments need `file_format: delta` (or another v2 format); Snowflake does not persist docs for mixed-case column names unless the YAML name is all lower/upper case or `quote: true` is set.

## Generate and host
```bash
dbt docs generate            # copies index.html into target/, writes manifest.json and catalog.json (queries database metadata)
dbt docs serve --port 8080   # local web server rooted in target/ (default port 8080); run generate first
```
`dbt docs generate --static` inserts `catalog.json` and `manifest.json` into `index.html`, producing a single page you can host on a cloud storage provider or share as a file. `dbt docs serve` is not supported in the Studio IDE.

## Coverage
- See the documentation-coverage-checks skill for measuring and enforcing description coverage.
- Document a column once in a docs block and reuse it with `doc()`, or use the dbt-codegen `upstream_descriptions` option when generating model YAML.

## Verify
- [ ] Table and column comments appear in the warehouse catalog after a build with `persist_docs` enabled.
- [ ] The docs site shows your descriptions and the `__overview__` landing page after `dbt docs generate`.

## Checked

2026-10-25: dbt docs, current branch of dbt-labs/docs.getdbt.com (last commit 2026-10-23). Confirmed: dbt documentation, `dbt docs` command and persist_docs pages: `doc()` and docs blocks in `.md` files, `__overview__`, `persist_docs: {relation, columns}` config, supported adapters, not implemented for sources, Databricks and Snowflake limitations, `dbt docs generate` outputs and `--static`, `dbt docs serve` default port 8080 and Studio IDE limitation. Removed unconfirmed hosting recipes, version gate for `--static`, third-party coverage tooling and an information_schema comment query.

Method: documentation only; no commands were run.
