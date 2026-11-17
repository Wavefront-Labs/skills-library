---
id: computing-software.data-engineering.etl-pipeline-design.extract-load-with-dlt
name: extract-load-with-dlt
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, dlthub, dlt, python-extract-load, incremental-loading]
level: practitioner
status: gated
description: "Build custom Python extract-load pipelines with dlt (dlthub): sources and resources, incremental cursors, schema inference and contracts, destinations and state."
sources:
  - https://dlthub.com/docs/intro
  - https://dlthub.com/docs/general-usage/incremental-loading
  - https://dlthub.com/docs/general-usage/schema-contracts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom extract-load with dlt (dlthub)

**Goal:** load an API or database that managed EL tools do not cover, with incremental state, schema evolution and normalisation handled by a library.

## Minimal pipeline
```python
import dlt
from dlt.sources.helpers import requests

@dlt.resource(primary_key="id", write_disposition="merge")
def tickets(updated_at=dlt.sources.incremental("updated_at", initial_value="2026-01-01T00:00:00Z")):
    url = "https://api.example.com/v1/tickets"
    params = {"updated_since": updated_at.last_value, "per_page": 100}
    while url:
        r = requests.get(url, params=params, headers={"Authorization": f"Bearer {dlt.secrets['api_token']}"})
        r.raise_for_status()
        yield r.json()["data"]
        url, params = r.json().get("next"), None

pipeline = dlt.pipeline(pipeline_name="helpdesk", destination="snowflake", dataset_name="raw_helpdesk")
info = pipeline.run(tickets())
print(info)
```
- `incremental` stores the cursor in pipeline state (kept in the destination), so reruns continue where they left off.
- `write_disposition`: `append`, `replace`, `merge` (needs primary_key or merge_key).
- Nested JSON is normalised into child tables (`tickets__tags`) linked by `_dlt_parent_id`.

Run here with dlt 1.31.0 and the DuckDB destination against a local HTTP server: the resource above (pointed at the local URL) loaded 5 tickets, a rerun after one new ticket gave 6 rows in `tickets`, nested `tags` landed in `tickets__tags` with `_dlt_parent_id`, and `_dlt_loads` showed both loads with status 0. The Snowflake destination, verified sources and secret names for it were not run (gated: unconfirmed, source is paywalled or blocked).

## Config and secrets
`.dlt/secrets.toml` locally; env vars in production (`SOURCES__HELPDESK__API_TOKEN`, `DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD`).

## Schema contracts
```python
@dlt.resource(schema_contract={"tables": "evolve", "columns": "freeze", "data_type": "freeze"})
```
`freeze` raises on new columns/type changes (checked: `Contract on columns with contract_mode=freeze is violated`); `discard_row` dropped the row carrying a new column and `discard_value` kept the row without the new field (checked). Use `freeze` for critical sources.

## Built-in sources
`dlt init sql_database snowflake` (the `init` and `pipeline drop` subcommands exist in the CLI), `rest_api` declarative source, filesystem, and verified sources (GitHub, Stripe, etc.) as starting points.

## Run in production
Orchestrate with Airflow/Dagster (dlt has helpers), or a plain container job. Inspect `load_info` and the `_dlt_loads` table for load status.

## Gotchas
- Cursor fields must be monotonic; APIs that sort loosely need a lag window (`lag` option or overlap) plus merge dedup.
- Deleting the pipeline working directory locally does not reset state stored in the destination; use `pipeline.drop()` / `dlt pipeline drop` deliberately.

## Verify
Run twice: second run loads only new/changed rows; `_dlt_loads` shows both loads with status 0.
