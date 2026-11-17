---
id: computing-software.data-engineering.dbt.selecting-sources-and-source-status
name: selecting-sources-and-source-status
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, source-selection, source-status, source-freshness, state-selection]
level: advanced
status: docs-checked
description: "Select dbt work by source: source: selectors, building only models downstream of fresher sources with source_status:fresher+, and freshness artifacts in jobs."
sources:
  - https://docs.getdbt.com/reference/node-selection/methods
  - https://docs.getdbt.com/reference/commands/source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selecting sources and source_status

**Goal:** run only what new raw data affects.

## source: method
```bash
dbt build --select source:stripe+            # everything downstream of any stripe table
dbt build --select source:stripe.charges+    # one table
dbt source freshness --select source:stripe
dbt ls --select source:* --resource-type source
```

## source_status (freshness-driven builds)
1. Previous run saved freshness: `dbt source freshness` writes the `sources.json` artifact (execution times and `max_loaded_at` dates); keep it in a state folder (here `prev_state/`).
2. Current run:
```bash
dbt source freshness
dbt build --select source_status:fresher+ --state prev_state
```
`source_status:fresher+` applies to dbt v1.11 and later; run `dbt source freshness` again so the current results can be compared with the previous ones. `DBT_ENGINE_STATE` can replace `--state`.

## Combine
```bash
dbt build --select "source_status:fresher+ state:modified+" --state prev_state
```
(Space = union; comma = intersection.)

## Gotchas
- A stale source (warn or error) makes `dbt source freshness` exit with a nonzero code; run it as its own step so the build still happens when you want it to.

## Checked
2026-11-01. Confirmed against the dbt node selector methods page and the `dbt source freshness` command page: `source:` selection, `source_status:fresher+` with `--state` (v1.11+), `sources.json`, union (space) and intersection (comma), nonzero exit on stale sources. Removed: `error`/`warn`/`pass` status values, `loaded_at_field` behaviour, the artifact-pairing rule for `--state` and the dbt Cloud automatic-run claim (not stated on those pages).
Method: documentation only; no commands were run.
