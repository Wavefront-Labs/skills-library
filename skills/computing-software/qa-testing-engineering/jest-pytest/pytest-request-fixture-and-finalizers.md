---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-request-fixture-and-finalizers
name: pytest-request-fixture-and-finalizers
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [request-fixture, addfinalizer, pytest-fixtures, fixture-introspection, pytest]
level: practitioner
status: verified
description: "Use pytest's request fixture: request.param, node and markers, config options, getfixturevalue, addfinalizer for teardown, and choosing finalizers versus yield."
sources:
  - https://docs.pytest.org/en/stable/reference/reference.html#request
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#adding-finalizers-directly
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The request fixture and finalizers (pytest)

## What `request` gives a fixture
```python
@pytest.fixture
def api_client(request):
    marker = request.node.get_closest_marker("role")          # @pytest.mark.role("admin")
    role = marker.args[0] if marker else "member"
    base = request.config.getoption("--base-url")              # CLI option
    client = ApiClient(base, role=role)
    request.addfinalizer(client.close)
    return client
```
Key attributes:
- `request.param`: value when the fixture is parametrized (or indirect).
- `request.node`: the test item (name, nodeid, markers, `user_properties`).
- `request.function`, `request.cls`, `request.module`: where the requesting test lives.
- `request.config`: options and ini values.
- `request.fixturename`, `request.scope`.
- `request.getfixturevalue("db")`: request a fixture dynamically (e.g. chosen by marker).

## addfinalizer vs yield
```python
@pytest.fixture
def two_servers(request):
    a = start_server("a")
    request.addfinalizer(a.stop)        # registered immediately: runs even if b fails to start
    b = start_server("b")
    request.addfinalizer(b.stop)
    return a, b
```
Finalizers run LIFO. With `yield`, code after `yield` does not run if setup raised before the yield; `addfinalizer` after each resource gives safe partial teardown.

## Test outcome in teardown
```python
# conftest.py
@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    rep = yield
    setattr(item, f"rep_{rep.when}", rep)
    return rep

@pytest.fixture
def browser(request):
    b = launch()
    yield b
    if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
        b.screenshot(f"artifacts/{request.node.name}.png")
    b.close()
```

## Gotchas
- `getfixturevalue` inside tests hides dependencies; prefer arguments.
- Scope mismatch: a session fixture cannot use function-scoped fixtures through `request` either (ScopeMismatch).

## Verify
Partial setup failures leave no running resources, and failure artifacts are attached via the report hook.
