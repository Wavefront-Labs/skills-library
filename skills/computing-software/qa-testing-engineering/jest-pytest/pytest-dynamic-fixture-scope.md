---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-dynamic-fixture-scope
name: pytest-dynamic-fixture-scope
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [dynamic-fixture-scope, fixture-scope, teardown-order, addfinalizer]
level: practitioner
status: verified
description: "Choose pytest fixture scope dynamically with a callable, order teardown safely (yield, addfinalizer, ExitStack) and handle errors in setup and teardown."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#dynamic-scope
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#safe-teardowns
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic fixture scope and teardown ordering

## Dynamic scope
```python
def determine_scope(fixture_name, config):
    if config.getoption("--keep-containers", None):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
def postgres():
    with PostgresContainer("postgres:16") as pg:
        yield pg
```
```python
def pytest_addoption(parser):
    parser.addoption("--keep-containers", action="store_true")
```
Useful to share expensive resources locally while keeping strict isolation in CI (or vice versa).

## Teardown order
Fixtures tear down in reverse order of setup (LIFO). Within one fixture, code after `yield` runs at teardown even if the test failed, but **not** if the fixture raised before `yield`.

## Safe teardowns: one resource per fixture
```python
@pytest.fixture
def user(api):
    u = api.create_user()
    yield u
    api.delete_user(u.id)

@pytest.fixture
def order(api, user):
    o = api.create_order(user.id)
    yield o
    api.cancel_order(o.id)
```
If `create_order` fails, `user` is still cleaned up. A single fixture creating both would leak the user.

## Multiple resources in one fixture
```python
from contextlib import ExitStack
@pytest.fixture
def env():
    with ExitStack() as stack:
        a = stack.enter_context(start_a())
        b = stack.enter_context(start_b())
        yield a, b
```
`request.addfinalizer(fn)` registers cleanup that runs even if later setup code in the fixture raises (register right after each acquisition).

## Errors
- Setup exception -> test reported as **error** (E), not failure.
- Teardown exception -> extra error reported for that test; other teardowns still run.

## Verify
Force the second resource to fail in setup: the first resource's cleanup log line still appears (`pytest -s --setup-show`).
