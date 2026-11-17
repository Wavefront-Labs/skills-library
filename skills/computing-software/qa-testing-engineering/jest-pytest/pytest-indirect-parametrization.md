---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-indirect-parametrization
name: pytest-indirect-parametrization
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [indirect-parametrization, pytest-parametrize, parametrized-fixtures, pytest-fixtures, pytest]
level: practitioner
status: verified
description: "Parametrize pytest fixtures: params on @pytest.fixture with request.param, indirect=True to route parametrize values through fixtures, and pytest_generate_tests."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#parametrizing-fixtures
  - https://docs.pytest.org/en/stable/example/parametrize.html#indirect-parametrization
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parametrized and indirect fixtures (pytest)

## Parametrized fixture: every test using it runs per param
```python
@pytest.fixture(params=["sqlite", "postgres"], ids=["sqlite", "pg"])
def db(request, tmp_path, pg_container):
    if request.param == "sqlite":
        yield connect(f"sqlite:///{tmp_path}/t.db")
    else:
        yield connect(pg_container.url)
```
Every test requesting `db` runs twice. Combine two parametrized fixtures = cartesian product.

## Indirect: parametrize values passed to a fixture
```python
@pytest.fixture
def user(request, make_user):
    return make_user(role=request.param)        # value from parametrize

@pytest.mark.parametrize("user", ["admin", "member"], indirect=True)
def test_dashboard_visible(user, client):
    assert client.as_user(user).get("/dashboard").status_code == 200
```
Selective indirect: `indirect=["user"]` when parametrizing several args and only some go through fixtures.
Use when the parameter needs expensive or stateful setup (create a user, start a server) rather than a plain value.

## Dynamic generation
```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--browsers", default="chromium")

def pytest_generate_tests(metafunc):
    if "browser_name" in metafunc.fixturenames:
        metafunc.parametrize("browser_name", metafunc.config.getoption("browsers").split(","))
```

## Scope interaction
With `scope="module"` parametrized fixtures, pytest groups tests to minimise setups (all tests with param A, then B).

## Gotchas
- `request.param` raises AttributeError when the fixture is used without parametrization; give a default via `getattr(request, "param", "member")`.
- Huge cartesian products from stacked parametrized fixtures; check `pytest --collect-only -q | tail -1`.

## Verify
`pytest --collect-only` shows the expected test ids per parameter, and expensive setup runs once per param per scope.
