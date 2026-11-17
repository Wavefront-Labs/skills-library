---
id: computing-software.web-development.fastapi.testing-testclient
name: testing-testclient
category: computing-software
field: web-development
product: fastapi
tags: [fastapi, testing, testclient, pytest, httpx, jsonable-encoder]
level: practitioner
status: docs-checked
description: "Test a FastAPI app with TestClient and pytest: plain def tests, test file layout, passing json, data, headers and cookies, and installing httpx."
sources: [https://raw.githubusercontent.com/fastapi/fastapi/master/docs/en/docs/tutorial/testing.md]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing with TestClient

## Method
- Install `httpx` (needed by `TestClient`) and `pytest`.
- `from fastapi.testclient import TestClient`, then `client = TestClient(app)`. It is the same as `starlette.testclient`.
- Name test functions `test_...` (pytest convention). They are normal `def`, and client calls are normal calls without `await`.
- Use `assert` on the response, as with `httpx`.
- Put tests in e.g. `app/test_main.py` in the same package and use a relative import to get `app` from `main`.

## Passing data
- Path or query parameters: add to the URL.
- JSON body: `json=` with a Python object such as a `dict`.
- Form data: `data=`.
- Headers: dict in `headers=`. Cookies: dict in `cookies=`.
- If unsure how, look up how httpx (or requests) does it; the design follows Requests.
- `TestClient` takes JSON-convertible data, not Pydantic models; convert a model with `jsonable_encoder`.

## Async needs
To call `async` functions in tests apart from requests (e.g. async database calls), see the advanced Async Tests page.

## Run
`pytest` (e.g. `uv run pytest`) finds and runs the tests.

## Checked
Read the cited FastAPI documentation page(s) in full and compared each rule against them; every claim kept is stated there.
Method: docs-only read of cited pages, 2026-11-08
