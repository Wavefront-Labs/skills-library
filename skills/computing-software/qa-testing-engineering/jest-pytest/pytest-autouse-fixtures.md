---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-autouse-fixtures
name: pytest-autouse-fixtures
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [autouse, pytest-fixtures, implicit-setup, isolation-fixtures]
level: practitioner
status: verified
description: "Use pytest autouse fixtures for setup every test needs (env isolation, freezing time, DB transaction rollback) while keeping scope, ordering and cost under control."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#autouse-fixtures-fixtures-you-don-t-have-to-request
  - https://docs.pytest.org/en/stable/reference/fixtures.html#fixture-instantiation-order
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autouse fixtures

```python
@pytest.fixture(autouse=True)
def _isolate_env(monkeypatch, tmp_path):
    monkeypatch.setenv("APP_HOME", str(tmp_path))
    monkeypatch.delenv("AWS_PROFILE", raising=False)
```
Every test in the fixture's visibility scope (module, class, conftest directory) gets it without naming it.

## Good uses
- Guardrails: block real network (`monkeypatch.setattr(socket, "socket", guard)`), or fail on unexpected warnings.
- Per-test DB transaction rollback in integration directories.
- Resetting global singletons / caches (`functools.cache` clear) between tests.

## Ordering
Autouse fixtures are instantiated **before** explicitly requested fixtures of the same scope; higher scopes (session, module) before lower. Dependencies still resolve first.

## Scoped autouse
```python
@pytest.fixture(scope="session", autouse=True)
def _migrate_db(django_db_setup): ...
```
Only put autouse in the narrowest conftest that needs it: an autouse DB fixture in the root conftest makes unit tests slow.

## Opting out
No direct opt-out flag. Patterns: check a marker inside the fixture.
```python
@pytest.fixture(autouse=True)
def _no_network(request, monkeypatch):
    if "allow_network" in request.keywords:
        return
    monkeypatch.setattr("socket.socket.connect", _refuse)
```

## Gotchas
- Autouse fixtures are invisible in test signatures: name them with a leading underscore and document in conftest.
- An autouse fixture that depends on an expensive fixture forces that cost on every test in scope.
- Use `pytest --setup-show` to see the hidden setup chain.

## Verify
`pytest --setup-show -k one_test` lists the autouse fixtures; unit tests stay fast.
