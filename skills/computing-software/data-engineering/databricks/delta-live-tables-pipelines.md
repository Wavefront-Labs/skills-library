---
id: computing-software.data-engineering.databricks.delta-live-tables-pipelines
name: delta-live-tables-pipelines
category: computing-software
field: data-engineering
product: databricks
tags: [databricks, delta-live-tables, dlt, lakeflow, declarative-pipelines, expectations, apply-changes-into, autoloader, streaming-tables, materialized-views, data-quality-constraints, medallion-architecture]
status: docs-checked
level: practitioner
description: "Build declarative Delta Live Tables / Lakeflow pipelines with expectations and CDC, and know what DLT handles vs manual Delta work."
sources:
  - https://docs.databricks.com/en/delta-live-tables/index.html
  - https://docs.databricks.com/aws/en/ldp/concepts
  - https://docs.databricks.com/aws/en/ldp/expectations
  - https://docs.databricks.com/aws/en/ldp/cdc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Delta Live Tables / Lakeflow — declarative pipelines, and their edges

**Goal:** use declarative pipelines where they remove real plumbing (Auto Loader ingestion, dependency inference, CDC handling, data quality gating) and recognize where a pipeline still needs a hand-written Spark job instead. Databricks now documents this surface as Spark Declarative Pipelines on Lakeflow (formerly Delta Live Tables); the Python decorators are shown as `@dp.*` in the current docs. Verify naming against your runtime version.

## 1. The core idea — declare the table, not the job
A pipeline is a set of Python/SQL dataset definitions (`@dp.table`, or `CREATE STREAMING TABLE` / `CREATE MATERIALIZED VIEW` SQL). While it runs, the pipeline analyzes the dependencies of the objects you defined and orchestrates execution order and parallelization automatically (per the Pipeline concepts page), rather than you declaring task order as in Workflows or Airflow. Dependencies are therefore implicit in what each query reads: a refactor that changes which table a query reads changes the graph, so review the resulting DAG in the pipeline UI after any such refactor.

## 2. Streaming tables vs materialized views vs views
- **Streaming table**: each record is processed exactly once, assuming an append-only source. Suited to ingestion and incremental processing of continuously growing data (bronze layer). Streaming tables are always defined against streaming sources.
- **Materialized view**: results are recomputed as needed to reflect the current state of the data. Suited to transformations, aggregations, and results consumed by multiple downstream datasets; use it when the query performs aggregations or joins, or the source can change through updates and deletes. The engine reprocesses only new or changed source data when possible.
- **View**: evaluated on demand and not persisted; usable only inside the same pipeline. Good for intermediate transformations and for checks with expectations.
- Match the type to whether correctness depends on seeing every individual append (streaming table) or the current derived state (materialized view).

## 3. Expectations — data quality as a pipeline primitive
```python
@dp.table
@dp.expect_or_drop("valid_order_id", "order_id IS NOT NULL")
@dp.expect_or_fail("positive_amount", "amount > 0")
@dp.expect("fresh_record", "event_time > current_date() - INTERVAL 7 DAYS")  # warn: invalid rows still written
def orders():
    return spark.readStream.table("raw_orders")
```
- `dp.expect` (SQL: `CONSTRAINT name EXPECT (expr)`) is the default warn action: invalid records are written to the target.
- `dp.expect_or_drop` (SQL: `... ON VIOLATION DROP ROW`) drops invalid records before they reach the target; the drop count is logged with the dataset metrics, so watch it.
- `dp.expect_or_fail` (SQL: `... ON VIOLATION FAIL UPDATE`) makes invalid records fail the update; manual intervention is needed before reprocessing, and no metrics are recorded for fail.
- An expectation name must be unique per dataset. Constraints must be valid SQL and cannot contain custom Python functions, external service calls or subqueries referencing other tables.
- In Python only, `expect_all`, `expect_all_or_drop` and `expect_all_or_fail` take a dictionary of name to constraint, so a set can be reused across datasets.
- Metrics appear in the Data quality tab of the pipeline UI (and the event log). Expectations are not supported with AUTO CDC FROM SNAPSHOT.
This does not replace a broader DQ framework (computing-software.data-engineering.data-quality.great-expectations-and-dq-frameworks) for cross-system or statistical checks; it gates rows inside the pipeline.

## 4. AUTO CDC (formerly APPLY CHANGES) — CDC without hand-written MERGE
```sql
CREATE OR REFRESH STREAMING TABLE customers;

CREATE FLOW customers_cdc_flow AS AUTO CDC INTO customers
FROM STREAM(customers_cdc)
KEYS (customer_id)
SEQUENCE BY sequence_num
STORED AS SCD TYPE 2;
```
The AUTO CDC APIs replace the APPLY CHANGES APIs and have the same syntax; APPLY CHANGES is still available but Databricks recommends AUTO CDC. It handles out-of-order CDC events and both SCD Type 1 and Type 2 without hand-written merge logic (see computing-software.data-engineering.data-modelling.dimensional-modelling-and-scd for the SCD Type 2 logic it replaces). `SEQUENCE BY` must identify event ordering correctly (a source timestamp or monotonic sequence; the docs also show `SEQUENCE BY STRUCT(timestamp_col, id_col)` for tie-breaking); test with deliberately reordered input before trusting a real feed. AUTO CDC is not available in open-source Spark Declarative Pipelines.

## 5. Where pipelines aren't the right tool
Highly custom branching logic, non-tabular outputs, workloads needing fine control over checkpoint/trigger behaviour beyond what pipelines expose, or integration with non-Databricks orchestration where pipeline-level scheduling does not fit are still better served by a hand-written Structured Streaming or batch job under a Lakeflow Job. Match pipelines to work that is genuinely declarative table-transformation shaped.

## Verify
- [ ] The pipeline DAG shown in the UI matches the intended dependency structure after any query refactor.
- [ ] `expect_or_drop` drop counts are monitored, not just logged and ignored.
- [ ] `SEQUENCE BY` was tested against deliberately out-of-order input and resolves correctly.
- [ ] Streaming-table vs materialized-view choice matches the table's correctness requirement (every append vs current state).

## Checked
Date: 2026-11-09. Confirmed against the Databricks pages in sources (Spark Declarative Pipelines on Lakeflow landing page, Pipeline concepts, Manage data quality with pipeline expectations, AUTO CDC): dataset type semantics, automatic dependency orchestration, expectation actions with SQL and Python syntax, uniqueness and constraint restrictions, expect_all variants, metrics location, AUTO CDC replacing APPLY CHANGES, SCD 1/2 and SEQUENCE BY STRUCT form, AUTO CDC absent from open-source SDP. Rewritten: legacy `@dlt` decorators and `APPLY CHANGES INTO live.` syntax replaced with the current forms; the 7-day expectation expression rewritten to the INTERVAL form the docs use. Removed: the silent-corruption wording for SEQUENCE BY. Not read: the Auto Loader and event-log pages.
Method: documentation only; no commands were run.
