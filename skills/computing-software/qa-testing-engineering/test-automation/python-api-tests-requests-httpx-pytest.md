---
id: computing-software.qa-testing-engineering.test-automation.python-api-tests-requests-httpx-pytest
name: python-api-tests-requests-httpx-pytest
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [httpx-tests, requests-api-tests, api-testing, pytest, python, rest-api]
level: practitioner
status: verified
description: "Write API tests in Python with requests or httpx and pytest: session fixtures, auth, base URLs, schema and value assertions, async tests, retries and logging."
sources:
  - https://www.python-httpx.org/
  - https://requests.readthedocs.io/
  - https://docs.pytest.org/en/stable/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API tests in Python with requests or httpx and pytest

**Goal:** a maintainable Python API suite: shared clients via fixtures, clear assertions, readable failures.

## Fixtures

```python
# conftest.py
import os, httpx, pytest

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("API_BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def token(base_url):
    r = httpx.post(f"{base_url}/auth/token", data={"username": os.environ["API_USER"], "password": os.environ["API_PASS"]})
    r.raise_for_status()
    return r.json()["access_token"]

@pytest.fixture
def api(base_url, token):
    with httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {token}"}, timeout=10) as c:
        yield c
```

## Tests

```python
def test_create_order_returns_201_and_location(api):
    r = api.post("/orders", json={"sku": "ABC", "qty": 2})
    assert r.status_code == 201, r.text
    assert r.headers["location"].startswith("/orders/")
    body = r.json()
    assert body["status"] == "PENDING" and body["qty"] == 2

@pytest.mark.parametrize("qty", [0, -1, 10_001])
def test_invalid_qty_rejected(api, qty):
    r = api.post("/orders", json={"sku": "ABC", "qty": qty})
    assert r.status_code == 422
```

- Include `r.text` in assertion messages so failures show the body. Run against a small FastAPI app (httpx 0.28.1, requests 2.34.2, pytest 9.1, pytest-asyncio): the fixtures and both tests above, the async test, and a `requests.Session` equivalent passed; a deliberately failing assert printed the 422 body with the `detail` list. `API_USER`/`API_PASS` must be set or the `token` fixture raises KeyError.
- requests equivalent: `requests.Session()` with `s.headers.update(...)`; requests has no base_url, so wrap with a small helper or use httpx.
- **Async:** `httpx.AsyncClient` with `pytest-asyncio` (`@pytest.mark.asyncio`, which works in the default strict mode; install `pytest-asyncio` or the test is not awaited) for concurrency tests.
- **Timeouts:** always set them; requests has none by default (its quickstart says requests will not time out unless `timeout` is given) and can hang a CI job. httpx defaults to 5 seconds.
- **Mocking downstreams in-process:** `respx` (httpx) or `responses` (requests).
- **Logging:** httpx event hooks (`event_hooks={"request": [...], "response": [...]}`, both fired in a run) to log request/response on failure; avoid logging tokens.
- Schema checks with `jsonschema`; cleanup created data via fixtures with `yield`.

## Verify
`pytest -q` runs against a configurable base URL, credentials come from environment variables, and a failing assertion prints the status and response body.
