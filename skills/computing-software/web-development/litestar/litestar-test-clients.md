---
id: computing-software.web-development.litestar.litestar-test-clients
name: litestar-test-clients
category: computing-software
field: web-development
product: litestar
tags: [litestar, testing, test-client, asynctestclient, websocket-connect, sessions, create-test-client]
level: practitioner
status: docs-checked
description: "Test Litestar apps with TestClient and AsyncTestClient, pytest fixtures, websocket_connect, session data helpers, blocking_portal and create_test_client."
sources: [https://docs.litestar.dev/latest/usage/testing.html]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litestar test clients

Goal: write sync or async tests against a Litestar app without running a server.

## Method

Install the extra (bundles httpx2): `pip install 'litestar[testing]'`.

Sync (`TestClient`) runs the app in a new event loop in a separate thread; async (`AsyncTestClient`) runs on an externally managed loop. Both have the same API:

```python
from litestar.testing import TestClient, AsyncTestClient

def test_health_check():
    with TestClient(app=app) as client:
        response = client.get("/health-check")
        assert response.status_code == HTTP_200_OK

async def test_health_check_async():
    async with AsyncTestClient(app=app) as client:
        response = await client.get("/health-check")
```

Wrap the client in a pytest fixture (`scope="function"`, yield inside the `with` / `async with`).

Choose `AsyncTestClient` when tests or fixtures run under anyio's pytest plugin or pytest-asyncio and share async resources (such as an `httpx2.AsyncClient`) with the app. With the sync client the app runs in a different event loop than the test, which in the page's example fails with `RuntimeError: Event loop is closed` on cleanup; switching to `AsyncTestClient` fixes it.

Other helpers:
- `create_test_client(route_handlers=[...])` builds a Litestar app and client in one call, good for isolated endpoint tests.
- WebSockets: `client.websocket_connect("/ws")` returns a connection with `send_json`, `receive_json`:

```python
with create_test_client(route_handlers=[websocket_handler]) as client, client.websocket_connect("/ws") as ws:
    ws.send_json({"hello": "world"})
    assert ws.receive_json() == {"message": {"hello": "world"}}
```

- Sessions: `TestClient(app=app, session_config=session_config)` exposes `client.set_session_data({...})` and `client.get_session_data()` (needs session middleware configured).
- Async code from a sync test: `client.blocking_portal.call(coro_fn, arg)` and `.start_task_soon(...)` run on the app's loop.
- Server-sent events with infinite generators lock up the in-process client; use `subprocess_sync_client` / `subprocess_async_client` (`workdir=...`, `app="module:app"`, `capture_output=False` to discard output).
- `RequestFactory().get("/")` builds a `Request` for unit-testing guards; use `handler.copy()` before changing `opt`.

## Verify

Per the example, the `/health-check` test passes with status 200 and body `healthy`; a session test sees `{"foo": "bar"}` after `set_session_data`.

## Checked

2026-11-07. Read the full cited page(s) (usage/testing.html) and the example files they include, and confirmed the claims in this skill against that text. Corrected httpx to httpx2 (the page's name for the bundled client and its AsyncClient).

Method: documentation only; no commands were run.
