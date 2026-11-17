---
id: computing-software.software-engineering.python.testing-async-code-with-pytest
name: testing-async-code-with-pytest
category: computing-software
field: software-engineering
product: python
tags: [python, pytest-asyncio, anyio, async-testing, asyncmock, event-loop-scope, pytest]
level: practitioner
status: verified
description: "Test asyncio code with pytest-asyncio or the anyio plugin: async tests and fixtures, loop scope, AsyncMock, and testing timeouts and cancellation without real sleeps."
sources: ["https://pytest-asyncio.readthedocs.io/en/stable/", "https://anyio.readthedocs.io/en/stable/testing.html", "https://docs.python.org/3/library/unittest.mock.html#unittest.mock.AsyncMock"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing async code with pytest

**Goal:** async tests that run fast, don't leak loops between tests, and exercise
timeout/cancellation paths deterministically.

## pytest-asyncio setup
```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"                         # every async def test/fixture is handled
asyncio_default_fixture_loop_scope = "function"
```
```python
async def test_fetch_user(client):
    user = await client.get_user(1)
    assert user.name == "Ada"
```
With `asyncio_mode = "strict"` (default) mark tests `@pytest.mark.asyncio` and fixtures
`@pytest_asyncio.fixture`.

## Async fixtures and loop scope
```python
import pytest_asyncio
@pytest_asyncio.fixture(loop_scope="session", scope="session")
async def db_pool():
    pool = await asyncpg.create_pool(DSN)
    yield pool
    await pool.close()

@pytest.mark.asyncio(loop_scope="session")
async def test_query(db_pool): ...
```
A session-scoped async resource must live on a session-scoped loop, and tests using it must
run on that same loop; otherwise "attached to a different loop" / "Future attached to a
different loop" errors.

## anyio alternative
```python
@pytest.mark.anyio
async def test_x(): ...
@pytest.fixture
def anyio_backend(): return "asyncio"      # or parametrize ["asyncio", "trio"]
```
Good for libraries supporting both asyncio and trio; it ships with httpx/starlette stacks.

## Mocking coroutines
```python
from unittest.mock import AsyncMock, patch
repo = AsyncMock()
repo.get_user.return_value = User(1, "Ada")        # awaited -> returns value
repo.save.side_effect = TimeoutError                # awaited -> raises
await service.rename(repo, 1, "Grace")
repo.save.assert_awaited_once()
```
`patch()` auto-uses AsyncMock when the target is an `async def`.

## Time and cancellation without sleeping
```python
async def test_times_out():
    async def hang():                       # an async side_effect is awaited; a sync lambda
        await asyncio.sleep(3600)            # returning a coroutine is NOT (test never raised)
    slow = AsyncMock(side_effect=hang)
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.01):
            await slow()
```
Keep timeouts injectable (parameter or setting) so tests use milliseconds. For clock-heavy
logic, `time-machine`/`looptime` fake the loop clock.

## Testing ASGI apps
```python
async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://t") as c:
    r = await c.get("/health")
```

## Verify
- [ ] Tests pass with `PYTHONASYNCIODEBUG=1 -W error::RuntimeWarning` (no un-awaited coroutines).
- [ ] No real `asyncio.sleep` > 0.1 s in the unit suite.

## Checked
- pytest 9.1.1, pytest-asyncio 1.4.0, anyio 4.15.1, httpx on Python 3.14.0: `asyncio_mode=auto` ran bare `async def` tests; default strict mode failed an unmarked async test; session-scoped async fixture with `loop_scope="session"` worked with a matching marker and a function-loop test using it failed; `AsyncMock` return and `side_effect` exceptions worked, `assert_awaited_once`, and `patch` of an async function produced an `AsyncMock`; the old lambda side_effect example never raised (fixed); `pytest.mark.anyio` with an `anyio_backend` fixture and `httpx.ASGITransport` worked; the suite passed with `-W error::RuntimeWarning` and `PYTHONASYNCIODEBUG=1`. `looptime` and `time-machine` exist on PyPI; neither was run. asyncpg was not run.
