---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-asyncio-async-tests
name: pytest-asyncio-async-tests
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, pytest-asyncio, asyncio, async-testing, async-fixtures, anyio, python]
level: practitioner
status: verified
description: "Test asyncio code with pytest-asyncio: asyncio mode, async fixtures, event loop scope, mocking coroutines with AsyncMock and timeouts for hanging awaits."
sources:
  - https://pytest-asyncio.readthedocs.io/en/stable/
  - https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing async code with pytest-asyncio

**Goal:** async tests and fixtures that run on a controlled event loop.

## Setup
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"                       # no need to mark every test
asyncio_default_fixture_loop_scope = "function"
```
```python
import pytest, asyncio
from unittest.mock import AsyncMock

async def test_fetch_user(client):
    user = await client.get_user(1)
    assert user.name == "Ada"

@pytest.fixture
async def client():
    c = await ApiClient.connect("http://localhost:8080")
    yield c
    await c.close()

async def test_retries_on_timeout():
    transport = AsyncMock(side_effect=[asyncio.TimeoutError, {"ok": True}])
    assert await fetch_with_retry(transport) == {"ok": True}
    assert transport.await_count == 2
```
In strict mode, mark tests with `@pytest.mark.asyncio` and fixtures with `@pytest_asyncio.fixture`.

## Loop scope
Session-scoped async fixtures (shared DB pool) need a matching loop scope: `@pytest_asyncio.fixture(loop_scope="session", scope="session")` and tests marked `@pytest.mark.asyncio(loop_scope="session")`. Mismatched scopes give "attached to a different loop" errors (reproduced by awaiting a session-loop future in a function-loop test).

## Timeouts
```python
async def test_does_not_hang():
    async with asyncio.timeout(2):       # Python 3.11+
        await worker.run_once()
```
Or `pytest-timeout` globally (`timeout = 30`).

## Alternative
AnyIO's pytest plugin (`@pytest.mark.anyio`) runs tests on asyncio and trio.

## Gotchas
- Forgetting `await` on a coroutine makes the test pass without running the code; run with `-W error` (or `filterwarnings = ["error"]`) so the "coroutine was never awaited" warning fails the test. Checked on pytest 9.1.1 and pytest-asyncio 1.4.0: pytest reports it as a `PytestUnraisableExceptionWarning`, so `-W error::RuntimeWarning` alone left the test passing.
- `MagicMock` for an async function returns a non-awaitable; use `AsyncMock` (plain `patch` on an `async def` returns an `AsyncMock` automatically, Python 3.8+).

## Verify
Remove an `await` in the code under test: a test or the `-W error` setting catches it.
