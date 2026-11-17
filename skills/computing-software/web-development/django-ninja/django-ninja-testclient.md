---
id: computing-software.web-development.django-ninja.django-ninja-testclient
name: django-ninja-testclient
category: computing-software
field: web-development
product: django-ninja
tags: [django-ninja, testing-client, testclient, testasyncclient, pytest, django-testcase]
level: practitioner
status: docs-checked
description: "Test Django Ninja APIs and routers with ninja.testing TestClient and TestAsyncClient: JSON, forms, query params, headers, user, files and async."
sources:
  - https://github.com/vitalik/django-ninja/blob/master/docs/docs/guide/testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: fast tests that call operation functions directly, skipping URL resolution and middleware.

## Basic
```python
from ninja.testing import TestClient

client = TestClient(api)   # a NinjaAPI or a bare Router

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
```
Works from Django `TestCase` with `self.assertEqual` too. Passing a `Router` builds a throwaway `NinjaAPI` without touching your router.

## Sending data
- `json=` (dict or `Schema`): `client.post("/echo", json={"name": "Ninja"})`
- `data=` form-style: `client.post("/items", data={"name": "Katana", "qty": 3})`
- Query: put it in the path or use `query_params={"category": ["tools", "outdoor"]}` (only used when path has no `?`; a list repeats the key)
- Files: `FILES={"file": SimpleUploadedFile("test.txt", b"data123")}`; use a `MultiValueDict` for several files under one field.
- Headers/cookies: `TestClient(router, headers={"A": "a"}, COOKIES={"A": "a"})`, overridable per request with `headers=`/`COOKIES=`.
- Any other keyword (not `data`, `json`, `headers`, `COOKIES`, `query_params`, `FILES`, `META`, `body`, `user`) is set as a request attribute, e.g. `client.get("/hello", company_id=1)`.

## Response (NinjaResponse)
`status_code`, `json()`, `data` (shortcut for `json()`), `content` (raw bytes), `response["Header-Name"]`.

## Authenticated views
By default `request.user` is an unauthenticated mock, so `auth=django_auth` rejects. Pass `user=`:
```python
def test_me(db):
    user = User.objects.create(username="ninja")
    response = client.get("/me", user=user)
```
API key/Bearer/Basic auth needs no setup; send real credentials as header, query param or cookie.

## Async
```python
from ninja.testing import TestAsyncClient
client = TestAsyncClient(api)

@pytest.mark.asyncio
async def test_hello():
    response = await client.get("/hello")
```
Needs an async runner such as `pytest-asyncio`.

## Tips
- For real middleware, CSRF enforcement or your URL conf, use Django's `django.test.Client`.
- A path matching no operation raises a plain `Exception`.
- DB access needs `TestCase` or pytest-django `db`/`transactional_db`.

## Checked

2026-11-08: Read django-ninja docs/docs/guide/testing.md from GitHub. Confirmed against the whole page: TestClient and TestAsyncClient usage, json/data/query_params/FILES/headers/COOKIES/user arguments, arbitrary request attributes, NinjaResponse members, and the tips. Nothing removed.

Method: documentation only; no commands were run.
