---
id: computing-software.data-engineering.dbt.dbt-retry-and-artifacts
name: dbt-retry-and-artifacts
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-retry, dbt-artifacts, run-results-json, manifest-json, sources-json, catalog-json, result-selector, elementary]
level: advanced
status: gated
description: "Recover and observe dbt runs: dbt retry from the point of failure, result:error+ selectors, and using run_results/manifest/sources/catalog artifacts for monitoring and lineage."
sources:
  - https://docs.getdbt.com/reference/commands/retry
  - https://docs.getdbt.com/reference/artifacts/dbt-artifacts
  - https://docs.getdbt.com/reference/node-selection/methods#result
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt retry and artifacts

**Goal:** resume a failed run without rebuilding what already succeeded, and turn dbt's JSON artifacts into monitoring data.

## dbt retry (introduced in 1.6 (gated: unconfirmed, source is paywalled or blocked))
```bash
dbt build --target prod        # fails at fct_orders, 40 other nodes skipped
# fix the cause (data, permissions, transient warehouse issue) then:
dbt retry                       # re-executes only errored and skipped nodes, same args/flags
```
`retry` reads `target/run_results.json` from the previous invocation: run it in the **same working directory** (or point `--state` at the saved artifacts). If the previous run succeeded, retry does nothing (it warned "Nothing to do"). Checked: after a build with one failed test and one skipped model, retry re-ran exactly those two nodes with the original `--vars`, and re-parsed the project, so a fixed config was picked up.

Alternative with selectors:
```bash
dbt build -s result:error+ result:fail+ result:skipped+ --state target/   # previous run artifacts as state; failed tests have status `fail`, so `result:error` alone misses them (checked with `dbt ls`)
```
Orchestrators: Airflow retries of a whole `dbt build` task rebuild everything; prefer a retry step calling `dbt retry`, or per-model tasks (Cosmos).

## Artifacts in target/
| File | Contents | Use |
|---|---|---|
| `manifest.json` | Full project graph, configs, compiled SQL (after compile/run) | State/defer, lineage, governance checks |
| `run_results.json` | Status, timing, rows affected, failures per node | Alerting, duration trends, retry |
| `sources.json` | Freshness results (`dbt source freshness`) (gated: unconfirmed, source is paywalled or blocked) | Freshness dashboards |
| `catalog.json` | Column types/stats from the warehouse (`dbt docs generate`) | Docs, catalog ingestion |
| `semantic_manifest.json` | Semantic layer definitions | MetricFlow |

## Monitoring patterns
- Upload `run_results.json` + `manifest.json` after each prod run to object storage; load them into the warehouse (the `dbt_artifacts` package does this in-run via on-run-end (gated: unconfirmed, source is paywalled or blocked)) and chart slowest models, failure counts, test failure trends.
- Elementary (dbt package + CLI) builds observability tables and Slack alerts from these (gated: unconfirmed, source is paywalled or blocked).
- Catalog tools (DataHub, OpenMetadata, Atlan) ingest manifest + catalog for lineage (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Artifacts are overwritten by every invocation in the same `target/` dir: copy them before running another command (or use `--target-path`).
- Artifact schema versions change across dbt versions; parsers must handle `dbt_schema_version` (dbt 1.12.6 wrote manifest v12 and run-results v6).

## Verify
- [ ] After a forced mid-run failure, `dbt retry` completes the rest without rebuilding successful nodes.
- [ ] Prod artifacts are archived per run and queryable for duration trends.
