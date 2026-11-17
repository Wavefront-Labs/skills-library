---
id: computing-software.data-engineering.dbt.dbt-build-command
name: dbt-build-command
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-build, fail-fast, skip-on-failure, empty-flag, full-refresh, sample-mode, threads, run-vs-build]
level: practitioner
status: verified
description: "Use dbt build as the default command: DAG-ordered models/tests/seeds/snapshots, downstream skipping on test failure, --fail-fast, --full-refresh, --empty and resource-type filters."
sources:
  - https://docs.getdbt.com/reference/commands/build
  - https://docs.getdbt.com/reference/global-configs/failing-fast
  - https://docs.getdbt.com/reference/commands/run#the---empty-flag
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt build

**Goal:** build and validate in one DAG-ordered pass so bad data stops at the node where it is detected.

## Why build instead of run + test
`dbt run && dbt test` builds everything first, then tests: a broken staging model has already propagated into marts. `dbt build` runs each node's tests right after it and **skips downstream nodes** when a test with `severity: error` fails (or a model errors).

```bash
dbt build                                   # models, tests, seeds, snapshots, (unit tests, saved queries)
dbt build -s +fct_orders --exclude-resource-type snapshot
dbt build --resource-type model --resource-type test
dbt build --fail-fast                       # stop the whole invocation at first failure (-x)
dbt build -s fct_events --full-refresh      # rebuild incrementals from scratch
dbt build -s +fct_orders --empty            # zero-row run to validate SQL/compile cheaply (compiled refs become `where false limit 0`)
dbt build --threads 16
```

## Reading results
- Exit code 0 = success; 1 = handled errors/failures; 2 = unhandled error (for example Ctrl-C or a network interruption; dbt docs, exit-codes page). Orchestrators should fail on non-zero. A bad `--warn-error-options` also exited 2.
- `target/run_results.json` lists each node with `status` (success/error/fail/warn/skipped) and timing.
- Skipped nodes show as `SKIP relation main.down` in the log; the reason ("Marking all children of 'test...' to be skipped because of status 'fail'") appears only at debug level (`--debug`).

## Choosing flags
| Need | Flag |
|---|---|
| CI fast feedback | `--fail-fast` |
| Prod nightly, keep going where possible | default (independent branches continue) |
| Validate SQL compiles against real schemas, no cost | `--empty` |
| Schema change on incremental | `--full-refresh` for the affected model only |
| Snapshots on a different cadence | `--exclude-resource-type snapshot` here, separate job for snapshots |

## Gotchas
- `--full-refresh` without `-s` rebuilds every incremental model: potentially huge cost. Guard in orchestration.
- Warnings (`severity: warn`) never block; review them or they rot.
- Tests depending on multiple models run after all their parents; a relationship test failure can skip unrelated children of the tested model.

## Verify
- [ ] Introduce a failing unique test on a staging model in dev: downstream marts show SKIP.
- [ ] Orchestrator marks the task failed on exit code 1.
