---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-conftest-layering-and-overrides
name: pytest-conftest-layering-and-overrides
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [conftest-layering, fixture-override, conftest, pytest-fixtures]
level: practitioner
status: verified
description: "Layer pytest conftest.py files by directory, override fixtures at module, class or parametrize level, and avoid conftest sprawl and import pitfalls."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#override-a-fixture-on-a-folder-conftest-level
  - https://docs.pytest.org/en/stable/reference/fixtures.html#conftest-py-sharing-fixtures-across-multiple-files
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# conftest.py layering and fixture overriding

## Visibility rules
- A fixture in `tests/conftest.py` is available to every test under `tests/`.
- `tests/api/conftest.py` fixtures are visible only under `tests/api/`.
- Lookup goes from the test outward: class -> module -> nearest conftest -> parent conftests -> plugins. The nearest definition wins.
- Never import from `conftest.py`; pytest loads it itself. Shared helpers go in a normal module (`tests/helpers.py`) or a plugin.

## Override by directory
```python
# tests/conftest.py
@pytest.fixture
def client(app): return app.test_client()

# tests/admin/conftest.py
@pytest.fixture
def client(client, admin_token):          # extend the parent fixture of the same name
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {admin_token}"
    return client
```
Requesting the same name as a parameter gives you the outer definition (super-call pattern).

## Override in a module or class
```python
@pytest.fixture
def settings(settings):
    return {**settings, "feature_x": True}
```

## Override with parametrize
Direct parametrization overrides a fixture value for that test:
```python
@pytest.mark.parametrize("username", ["bob"])
def test_profile(user):        # user fixture depends on username fixture
    assert user.name == "bob"
```

## Layout guidance
```
tests/
  conftest.py          # app, db, client: broadly shared
  unit/conftest.py     # fakes only
  integration/conftest.py   # real services, testcontainers
```
Use `pytest --fixtures tests/admin` to list what a directory sees and where each fixture is defined (`-v` adds file locations).

## Gotchas
- A `conftest.py` only applies to tests collected under its directory (an `admin/conftest.py` override is invisible to `other/` tests).
- `rootdir`-level conftest in a monorepo affects every package; keep it minimal.
- `pytest_plugins = [...]` in a non-top-level conftest is an error ("Defining 'pytest_plugins' in a non-top-level conftest is no longer supported"); declare it in the top-level conftest.

## Verify
`pytest --fixtures-per-test tests/admin/test_x.py` shows the overriding fixture's location.
