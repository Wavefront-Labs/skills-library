---
id: computing-software.data-engineering.etl-pipeline-design.metadata-driven-pipelines
name: metadata-driven-pipelines
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, orchestration, metadata-driven-pipelines, config-driven, pipeline-generation, control-tables, yaml-config, dag-factory, schema-validation]
level: practitioner
status: draft
description: "Build config/metadata-driven pipelines: one tested generic loader driven by validated YAML or control tables, generated orchestration, versioned configs, and when this pattern backfires."
sources:
  - https://learn.microsoft.com/en-us/azure/data-factory/copy-data-tool-metadata-driven
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/dynamic-dag-generation.html
  - https://docs.pydantic.dev/latest/
  - https://dlthub.com/docs/general-usage/source
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Metadata-driven pipelines

**Goal:** onboard the 50th table or source by adding a config entry, not by copy-pasting a pipeline — while keeping each table's behaviour explicit, validated and reviewable.

## 1. When it fits
Good: many similar flows differing only in parameters (ingest 300 tables from the same database, land 40 partner feeds of the same shape, apply standard bronze→silver cleansing).
Bad: flows with genuinely different logic — forcing them into config produces a config language with `if` flags that nobody can test. Keep bespoke logic in code.

## 2. Config as code, validated
```yaml
# configs/sources/erp.yaml
source: erp
connection: erp_replica
defaults: {load_type: incremental, schedule: "0 2 * * *", target_schema: raw_erp}
tables:
  - name: orders
    primary_key: [order_id]
    watermark_column: updated_at
  - name: customers
    primary_key: [customer_id]
    load_type: full
    pii_columns: [email, phone]
```
```python
from pydantic import BaseModel, model_validator
from typing import Literal
class TableCfg(BaseModel):
    name: str
    primary_key: list[str]
    load_type: Literal["incremental", "full", "cdc"] = "incremental"
    watermark_column: str | None = None
    pii_columns: list[str] = []
    @model_validator(mode="after")
    def check(self):
        if self.load_type == "incremental" and not self.watermark_column:
            raise ValueError(f"{self.name}: incremental needs watermark_column")
        return self
```
Validate in CI (schema + referential checks: connection exists, target schema allowed). Configs live in Git and change through PRs; avoid editing control tables by hand in prod.

## 3. One generic, well-tested loader
- A single function/operator per load type (`load_incremental(cfg)`, `load_full(cfg)`), unit-tested against representative configs.
- It handles: extraction query generation, watermark state, idempotent write (MERGE on `primary_key`), audit columns, PII masking, metrics, and errors per table (one table failing doesn't kill all).

## 4. Generate the orchestration
```python
# Airflow: one DAG per source, one mapped task per table
with DAG("ingest_erp", schedule=cfg.defaults.schedule, ...) as dag:
    load_table.expand(table_cfg=[t.model_dump() for t in cfg.tables])
```
Alternatives: Databricks for-each task over a config list; ADF Lookup + ForEach over a control table; Dagster asset factories. Keep generated objects named deterministically from config (`ingest_erp.orders`) so alerts and lineage are readable.

## 5. Control/state tables
Keep **runtime state** (last watermark, last run status, row counts) in a state table — separate from **desired config** in Git. Never store state in the config file.

## 6. Pitfalls
- Debuggability: log the fully resolved config for every run.
- Blast radius: a bad default change affects every table — require tests that render all configs and diff the generated plan in PRs.
- Escape hatch: allow a table to opt out to a custom pipeline cleanly.

## Verify
- [ ] Adding a table is a config-only PR that passes CI validation.
- [ ] CI renders the full plan (all generated tasks) and fails on invalid config.
- [ ] One failing table doesn't block others; failures name the table.
