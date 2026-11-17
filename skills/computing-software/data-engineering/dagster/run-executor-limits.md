---
id: computing-software.data-engineering.dagster.run-executor-limits
name: run-executor-limits
category: computing-software
field: data-engineering
product: dagster
tags: [dagster, max-concurrent, multiprocess-executor, executor, tag-concurrency, run-config]
level: practitioner
status: docs-checked
description: "Limit parallel ops inside a single Dagster run with max_concurrent run config and tag limits on the executor."
sources:
  - https://docs.dagster.io/guides/operate/managing-concurrency/run-executor-limits
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Run executor limits

Concurrency pool limits cap ops executing across all runs. To limit ops or assets executing within a single run, configure the run executor with `max_concurrent` in the run config, either in Python or in the Launchpad in the UI.

- The default depends on the run executor; `multiprocess_executor` by default limits executing ops to `multiprocessing.cpu_count()` in the launched run.
- Scope options in the docs: a specific job, or all runs in a code location (executor defined in the code location).
- Tag limits within a single run: multiple ops can run in parallel but only N with a given tag. Useful when ops in the same run have different resource requirements.

## Checked
2026-11-08. Confirmed against the Dagster docs page Run executor limits (raw markdown from the docs repo). Removed an unsupported closing advice sentence about memory/CPU; the code examples are referenced by file and were not read.
Method: documentation only; no commands were run.
