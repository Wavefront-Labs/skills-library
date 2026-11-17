---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-monkeypatch
name: pytest-monkeypatch
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [monkeypatch-setenv, monkeypatch, setattr, delenv, chdir]
level: practitioner
status: verified
description: "Use pytest monkeypatch to set and delete env vars, patch attributes and dict items, change cwd and sys.path, with automatic undo and the patch-where-used rule."
sources:
  - https://docs.pytest.org/en/stable/how-to/monkeypatch.html
  - https://docs.pytest.org/en/stable/reference/reference.html#monkeypatch
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# monkeypatch for env vars, attributes and dict items

All changes are undone after the test (function-scoped fixture).

```python
def test_config(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.delenv("HOME", raising=False)
    monkeypatch.setenv("PATH", "/opt/tool/bin", prepend=os.pathsep)
    monkeypatch.setattr("app.clock.now", lambda: datetime(2024, 1, 1))   # string target
    monkeypatch.setattr(app.settings, "TIMEOUT", 1)
    monkeypatch.setitem(app.settings.FLAGS, "beta", True)
    monkeypatch.delitem(os.environ, "DEBUG", raising=False)
    monkeypatch.chdir(tmp_path)
    monkeypatch.syspath_prepend(str(fixtures_dir))
```

## Patch where it is looked up
```python
# app/report.py
from requests import get
def fetch(): return get("https://x").json()
```
Patch `app.report.get`, not `requests.get`; the module already holds its own reference.

## Broader scope
`monkeypatch` is function-scoped. For module/session use the context manager:
```python
@pytest.fixture(scope="module")
def patched():
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("APP_ENV", "test")
        yield
```

## Blocking real network as a safety net
```python
@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    monkeypatch.delattr("requests.sessions.Session.request")
```

## monkeypatch vs unittest.mock
monkeypatch replaces values; it doesn't record calls. Need call assertions? Use `mocker`/`unittest.mock` (or setattr a `Mock`).

## Gotchas
- `setenv` values must be strings (pytest warns otherwise).
- Patching builtins like `open` is global and hits every caller; patch the module attribute (`app.io.open`) instead.
- Values read at import time (module-level constants computed from env) won't see later setenv: reload the module or restructure.

## Verify
After the test, `os.environ` is unchanged (another test asserting the original value passes in any order).
