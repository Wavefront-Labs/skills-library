---
id: computing-software.data-engineering.dbt.empty-and-sample-builds-for-ci
name: empty-and-sample-builds-for-ci
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, slim-ci, dbt-empty-flag, dbt-sample-mode, dbt-ci-job, schema-only-build, cost-control, event-time]
level: practitioner
status: verified
description: "Make dbt CI fast and cheap with --empty (schema-only builds), --sample with event_time (time-sliced data), and limits-in-dev patterns, and know what each does not test."
sources:
  - https://docs.getdbt.com/reference/commands/build#the---empty-flag
  - https://docs.getdbt.com/docs/build/sample-flag
  - https://docs.getdbt.com/reference/resource-configs/event-time
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# --empty and --sample builds for CI

**Goal:** validate SQL, contracts and DAG wiring on every PR in minutes, without rebuilding full tables.

## --empty
```bash
dbt build -s state:modified+ --defer --state prod-artifacts --empty
```
dbt wraps every `ref()`/`source()` in a `where false limit 0` subquery, so models are created with correct schemas and zero rows.
- Catches: syntax errors, missing columns, type/contract violations at DDL level, broken refs, permission errors.
- Misses: data tests are trivially passing on empty tables; logic bugs; incremental behaviour. The compiled SQL was `from (select * from "dev"."main"."stg_orders" where false limit 0) o` (checked).
- Use it to create schema-correct parents so **unit tests** (which need upstream relations for type inference) can run.

## --sample (needs `event_time`; `event_time` itself is documented from dbt 1.9)
```yaml
# configure event_time on models/sources that should be time-sliced
models:
  - name: stg_events
    config: {event_time: event_ts}
sources:
  - name: raw
    tables:
      - name: events
        config: {event_time: _loaded_at}
```
```bash
dbt build -s state:modified+ --sample="3 days"
dbt build --sample="{'start': '2026-10-01', 'end': '2026-10-08'}"
```
Refs/sources with `event_time` get filtered to the window; others are read in full. Data tests now run on real (recent) data. Same `event_time` config powers microbatch. Checked with `dbt run --sample`: `"3 days"` against 2026-09 data returned 0 rows, `"2 years"` all 20, and the explicit window `{'start': '2026-09-01', 'end': '2026-09-05'}` returned 4 rows (the end is exclusive). `--sample` is accepted by `run`/`build`, not `compile`.

## Older/manual pattern: limit in dev
```sql
select * from {{ source('raw', 'events') }}
{% if target.name in ['dev', 'ci'] %}
where _loaded_at >= dateadd(day, -3, current_date)
{% endif %}
```
Works on any version but scatters environment logic through models; prefer `--sample` where available.

## Suggested CI layering
1. `dbt parse` + pre-commit (seconds).
2. `dbt build --empty` on modified+ (schema check, unit tests).
3. `dbt build --sample "3 days"` on modified+ with data tests, or full build on modified models only for small projects.
4. Optional data diff of modified marts against prod.

## Gotchas
- `--empty` and incremental models: builds create the target empty; `is_incremental()` false. Fine for CI.
- `--sample` does not filter models without `event_time` (e.g. dimensions): they read full sources.
- Seeds: `dbt seed --empty` loaded zero rows on dbt 1.12.6 and emptied an existing seed table. Snapshots: behaviour with `--empty` is not described in the docs; test before relying on it.
- Results of sampled builds are not representative for uniqueness across the full table (duplicates outside the window are missed).

## Verify
- [ ] CI runtime and warehouse cost per PR measured before/after.
- [ ] A deliberately broken column reference fails the `--empty` step.
