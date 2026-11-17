---
id: computing-software.data-engineering.prefect.run-logging
name: run-logging
category: computing-software
field: data-engineering
product: prefect
tags: [logging, get-run-logger, log-prints, context, flow-run-logs]
level: practitioner
status: docs-checked
description: "Log from Prefect flows and tasks with get_run_logger and log_prints, fix missing context in hooks, threads and subprocesses, read logs by CLI."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/add-logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get logs into the Prefect backend and UI.

`get_run_logger()` (from `prefect.logging`) works inside a flow or task. In a task, records link to the flow run and task run; in a flow, to the flow run only.

```python
from prefect import flow
from prefect.logging import get_run_logger

@flow
def f():
    get_run_logger().info("INFO level log message.")
```

`print` output: set `log_prints=True` on a flow or task. Nested flows and tasks inherit it; set `log_prints=False` on a child to opt out. Global default:

```bash
prefect config set PREFECT_LOGGING_LOG_PRINTS=True
```

Missing context (`MissingContextError`):
- State change hooks: use `flow_run_logger` or `task_run_logger` from `prefect.logging.loggers`.
- Subprocesses: wrap the worker function with `with_context` from `prefect.context`, for example `pool.map(with_context(process_item), items)`; works with `multiprocessing.Pool`, `ProcessPoolExecutor` and `Process`.
- Manually created threads: the context lives in `contextvars`; use `copy_context()` and `ctx.run(...)`, or prefer `ThreadPoolTaskRunner`, which propagates it.

`get_logger()` returns a normal Python logger with the same configuration that does not send records to the Prefect API.

Read logs: `prefect flow-run logs MY-FLOW-RUN-ID`.

## Checked
2026-11-08. Confirmed against the add-logging how-to: get_run_logger scope, log_prints inheritance and PREFECT_LOGGING_LOG_PRINTS, MissingContextError cases and the flow_run_logger, with_context and copy_context fixes, ThreadPoolTaskRunner advice, get_logger not sending to the API, and prefect flow-run logs. Nothing removed.
Method: documentation only; no commands were run.
