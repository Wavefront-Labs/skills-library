---
id: computing-software.data-engineering.etl-pipeline-design.managed-el-tools-fivetran-airbyte
name: managed-el-tools-fivetran-airbyte
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, extraction, fivetran, airbyte, dlt-hub, elt]
level: practitioner
status: docs-checked
description: "Managed EL tools: Fivetran history mode (SCD2 columns, MAR cost, re-syncs), Airbyte sync modes, and what the dlt library does."
sources:
  - https://fivetran.com/docs/core-concepts
  - https://fivetran.com/docs/core-concepts/sync-modes/history-mode
  - https://docs.airbyte.com/using-airbyte/core-concepts/sync-modes
  - https://dlthub.com/docs/intro
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed EL tools: Fivetran, Airbyte, dlt

**Goal:** get SaaS and database data into the warehouse with the least custom code, while understanding how each tool treats history, deletes and re-syncs.

## 1. Fivetran
- **History mode** implements SCD Type 2: every version of each source record is written to the destination table, so you can analyse data at a point in time or how it changed. Available only for select connectors; soft delete mode is available for the vast majority. Check the connector page Features table and the connection Schema tab.
- Cost: enabling history mode on tables that change often can raise MAR (monthly active rows) usage, because each source insert or update becomes a new destination row and every new row counts toward paid MAR. For connectors that sync history tables by default, disable the tables in the Schema tab to avoid paid MAR.
- Where Fivetran defines the schema, history tables are predefined and cannot be changed; where it replicates your schema, you choose which tables track history. Tables with a `_history` suffix support history mode only, but not every history table has the suffix.
- System columns: `_fivetran_active` (TRUE only for the current version), `_fivetran_start` (replaces the source timestamp column), `_fivetran_end` (time the record stopped being active minus epsilon; active records get 9999-12-31T23:59:59.999Z on most destinations and 2038-01-19T03:14:07.999Z on MySQL). Deleted records get the delete timestamp minus one millisecond.
- A re-sync or table re-sync in history mode marks all previous records inactive and starts history again from the re-sync; the system columns are changing during a re-sync, so downstream code must not rely on them until it completes. A re-sync in general invalidates incremental cursors and re-fetches all records, overwriting existing rows.
- Limitations: tables lacking a monotonically increasing timestamp column, and re-imported tables (fully synced each time), are unsupported; Apache Kafka destinations do not support history mode. Without source change logs, intermediate changes between syncs are not captured (Salesforce is the cited example; sync more often to mitigate). History starts only from when a table is switched to history mode.
- Preview connectors: MAR are free during Private Preview and Public Preview.

## 2. Airbyte sync modes
- A sync mode combines how the source is read and how the destination is written.
- Source side: Incremental (records added since the last sync; the first incremental sync equals a full refresh; via a cursor, or via CDC on some sources) or Full Refresh (read everything).
- Destination side: Overwrite, Append, Append Deduped (history appended, final table de-duplicated by primary key) and Overwrite Deduped.
- Options shown in the UI when both connectors support them: Incremental Append, Incremental Append + Deduped, Full Refresh Append, Full Refresh Overwrite, Full Refresh Overwrite + Deduped.

## 3. dlt
An open-source Python library that loads data from sources such as REST APIs, SQL databases, cloud storage and Python data structures into structured datasets. It infers schemas and data types, normalises nested data, supports incremental loading, schema evolution and schema and data contracts, and can be deployed anywhere Python runs, including Airflow and serverless functions. Install with `pip install dlt`.

## Verify
For history tables, exactly one row per primary key has `_fivetran_active = TRUE`; for Airbyte streams the chosen sync mode matches the intended delete and history behaviour.

## Checked
Method: docs-only read on 2026-11-09 of the Fivetran history mode page (first ~150 lines of extracted text, through Limitations and Record history), the Airbyte sync modes page and the dlt intro page in full, and grep of the Fivetran core-concepts page (re-sync and MAR lines only). Dropped the Fivetran usage-based-pricing source (not read). Removed as unstated: build-vs-buy table, `_fivetran_synced`/`_fivetran_deleted` and Airbyte metadata column details, dlt merge and incremental code, configuration and operations advice, and tags source-systems, saas-connectors, monthly-active-rows and schema-drift.
