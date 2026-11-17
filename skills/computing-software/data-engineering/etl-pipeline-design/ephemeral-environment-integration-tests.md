---
id: computing-software.data-engineering.etl-pipeline-design.ephemeral-environment-integration-tests
name: ephemeral-environment-integration-tests
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, dataops, pipeline-testing, ephemeral-environments, integration-testing, testcontainers, zero-copy-clone, ci-cd, pr-schemas]
level: practitioner
status: draft
description: "Run pipeline integration tests in throwaway environments: per-PR schemas or zero-copy clones, Testcontainers for sources, seeded inputs, assertions, and guaranteed teardown."
sources:
  - https://testcontainers.com/guides/getting-started-with-testcontainers-for-python/
  - https://docs.snowflake.com/en/user-guide/object-clone
  - https://docs.getdbt.com/docs/deploy/continuous-integration
  - https://docs.databricks.com/aws/en/delta/clone
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Integration tests with ephemeral environments

**Goal:** every pipeline change runs end to end against real engines, in an environment created for that run and destroyed after, so tests never touch prod and never collide with each other.

## 1. Pick the isolation unit
| Layer | Ephemeral unit | Create | Destroy |
|---|---|---|---|
| Source DB (Postgres/MySQL) | container | Testcontainers / docker compose | container exit |
| Kafka | container (`confluentinc/cp-kafka`, Redpanda) | Testcontainers | container exit |
| Snowflake | schema or database clone | `CREATE DATABASE ci_pr_123 CLONE analytics;` | `DROP DATABASE ci_pr_123;` |
| Databricks | schema in a CI catalog, shallow clones | `CREATE TABLE ci.pr_123.orders SHALLOW CLONE prod.sales.orders;` | `DROP SCHEMA ci.pr_123 CASCADE;` |
| BigQuery | dataset with default table expiration | `bq mk --default_table_expiration 86400 ci_pr_123` | expiry or `bq rm -r -f` |
| dbt | `schema: dbt_ci_pr_<n>` target + `--defer --state` | CI job | `drop_schema` run-operation |

Name everything with the PR/run ID so concurrent runs cannot clash, and so a sweeper can find leftovers.

## 2. Testcontainers pattern (Python)
```python
import pytest, sqlalchemy as sa
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def source_db():
    with PostgresContainer("postgres:16") as pg:
        eng = sa.create_engine(pg.get_connection_url())
        with eng.begin() as c:
            c.execute(sa.text(open("tests/fixtures/source_schema.sql").read()))
            c.execute(sa.text(open("tests/fixtures/source_rows.sql").read()))
        yield eng

def test_extract_load(source_db, warehouse_schema):
    run_pipeline(source=source_db.url, target_schema=warehouse_schema)
    assert row_count(warehouse_schema, "orders") == 42
    assert no_duplicate_keys(warehouse_schema, "orders", "order_id")
```
Pin image tags; `latest` breaks CI on someone else's release day.

## 3. What to assert
- Row counts and key uniqueness per output table.
- A golden-file comparison for a small, hand-checked output (sorted CSV/Parquet).
- Idempotency: run the pipeline twice, assert outputs identical.
- Incremental path: load batch 1, then batch 2 with updates/deletes, assert final state.
- Schema: output columns and types match the contract.

## 4. Teardown and cost
- Teardown in `finally`/fixture finalisers **and** a scheduled sweeper that drops `ci_pr_*` objects older than 24 h — crashed runners skip finalisers.
- Use clones (metadata-only) rather than copies; sample large tables (`TABLESAMPLE`, date filter) when a full clone would make compute slow.
- Use an XS warehouse / small serverless budget for CI; set a statement timeout.
- Grant the CI identity create/drop only inside the CI database or catalog.

## Verify
- [ ] Two PRs running at once do not see each other's tables.
- [ ] Killing a run mid-way leaves objects the sweeper later removes.
- [ ] CI identity cannot write to prod objects (try it).
- [ ] The test fails when you deliberately break a join key.
