---
id: computing-software.data-engineering.dbt.project-run-performance
name: project-run-performance
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-performance, model-timing, threads, critical-path, partial-parse, query-tags, incremental-conversion, run-results-json]
level: advanced
status: docs-checked
description: "Speed up dbt runs: find the slowest nodes and critical path from run_results timing, and cut parse time with partial and static parsing."
sources:
  - https://docs.getdbt.com/reference/artifacts/run-results-json
  - https://docs.getdbt.com/reference/parsing
  - https://docs.getdbt.com/docs/deploy/run-visibility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dbt project run performance

**Goal:** shorten wall-clock time of the production run with measured changes.

## 1. Measure
`target/run_results.json` records every executed node: `unique_id`, `status`, `thread_id`, `execution_time` and a `timing` array (usually compile + execute). Top-level `elapsed_time` is the total invocation time. Only executed nodes appear, so separate `run` and `test` steps produce separate files.
```python
import json
rr = json.load(open("target/run_results.json"))
rows = sorted(((r["execution_time"], r["unique_id"]) for r in rr["results"]), reverse=True)
for t, n in rows[:20]: print(f"{t:8.1f}s {n}")
```
`adapter_response` carries adapter-specific metadata (for example `rows_affected`, `bytes_processed`).

dbt platform (Starter, Enterprise and above): the **Model timing** tab on a job run shows metric tiles (estimated critical path, peak concurrency, longest model, wall clock), a Gantt-style execution timeline (group by resource type, folder, phase or thread; highlight the critical path), a concurrency-over-time chart and a resource table. The estimated critical path is the longest chain of dependent models.

## 2. Parse time
At the start of every invocation dbt reads all project files and builds the manifest, which can be slow in big projects. Optimizations:
- **LibYAML:** PyYAML uses the C LibYAML if present. Test with `python -c "from yaml import CLoader"`.
- **Partial parsing:** dbt stores its manifest in `partial_parse.msgpack` and re-parses only changed files. On by default since v1.0 (`PARTIAL_PARSE` global config). Keeping `target/` between runs preserves it.
- **Static parser:** uses tree-sitter for models whose Jinja is only `ref`, `source` and `config`; on by default (`STATIC_PARSER`), at least 3x faster than a full Jinja render.

A full re-parse is triggered when `--vars`, `profiles.yml` content, `dbt_project.yml` content (or env vars used in them), installed packages, dbt version, or certain widely used macros (builtins, overrides, `generate_x_name`) change. Env vars used in models only re-parse the files that use them. CI gets no partial-parse benefit on a new PR or branch, only on later commits.

Do not use volatile context variables (`run_started_at`, `invocation_id`, `flags`) to set parse-time dependencies, configs or properties: with partial parsing they can go stale.

If partial parsing misbehaves (nodes not found, wrong configs), run with `--no-partial-parse` or `dbt clean` to delete `partial_parse.msgpack`. dbt v2 jobs no longer accept `--partial-parse`/`--no-partial-parse` (deprecation warning dbt1700).

## Verify
- [ ] Top-20 slowest nodes reviewed with owners.
- [ ] Wall time (`elapsed_time`) trend tracked after changes.

## Checked

2026-11-09. Pages read in full against this skill:
- https://docs.getdbt.com/reference/artifacts/run-results-json
- https://docs.getdbt.com/reference/parsing
- https://docs.getdbt.com/docs/deploy/run-visibility

Confirmed: the run_results fields, the Model timing tab contents, partial/static parsing defaults and the re-parse triggers.
Removed or reworded: the fix table (incremental conversion, view stacking, test filters), the threads/warehouse concurrency guidance, the query tag and query-comment cost attribution, `perf_info.json`, and the claim that `run_query` outside `execute` hurts parse time; none appears on the cited pages. The earlier claim that env var changes force full parses was narrowed to profiles/project files.

Method: documentation only; no commands were run.
