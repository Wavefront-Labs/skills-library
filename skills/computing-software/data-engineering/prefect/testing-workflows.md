---
id: computing-software.data-engineering.prefect.testing-workflows
name: testing-workflows
category: computing-software
field: data-engineering
product: prefect
tags: [testing, test-harness, pytest, fn, caplog]
level: practitioner
status: docs-checked
description: "Test Prefect flows and tasks with prefect_test_harness, a session pytest fixture, task.fn, disable_run_logger and the harness caveats."
sources:
  - https://docs.prefect.io/v3/how-to-guides/workflows/test-workflows
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run Prefect code in pytest against a throwaway server.

`prefect_test_harness` (from `prefect.testing.utilities`) runs flows and tasks against a temporary local SQLite database, using a subprocess server on a random port in the 8000-9000 range.

```python
@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture():
    with prefect_test_harness():
        yield
```

Skip the engine with `my_task.fn()`: it calls the wrapped function directly, skipping state tracking, retries and logging. If the function calls `get_run_logger()`, wrap the call in `disable_run_logger()` or you get `MissingContextError`.

Logs: pytest `caplog` captures flow and task logs only while the run logger is enabled.

Async: use `pytest-asyncio` with a synchronous harness fixture; mark tests `@pytest.mark.asyncio` and `await` the flow or a task's `.fn()`.

Caveats:
- Startup timeout is 30 seconds; raise with `prefect_test_harness(server_startup_timeout=60)`.
- Port conflicts: up to 10 random ports are tried.
- Python needs `sqlite3`.
- A session fixture shares one database; use a function-scoped harness in a separate module for isolation.
- Do not nest harnesses; the inner exit stops the shared server.
- With `pytest-xdist` each worker gets its own harness.

## Checked
2026-11-08. Confirmed against the test workflows how-to: prefect_test_harness, the session fixture, .fn(), disable_run_logger, caplog behaviour, async testing, 30 second startup timeout and server_startup_timeout, port range with up to 10 retries, sqlite3 requirement, nesting warning and pytest-xdist advice. Removed the step-by-step description of harness internals (environment variable names, cleanup order) because that section of the page is not readable.
Method: documentation only; no commands were run.
