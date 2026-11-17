---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-mock-mocker
name: pytest-mock-mocker
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-mock, mocker, mocker-spy, mocking, autospec]
level: practitioner
status: verified
description: "Use pytest-mock's mocker fixture (patch, patch.object, spy, stub, autospec) for automatic undo, call assertions and checking real behaviour with spies."
sources:
  - https://pytest-mock.readthedocs.io/en/latest/usage.html
  - https://docs.python.org/3/library/unittest.mock.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest-mock mocker fixture

```bash
pip install pytest-mock
```
`mocker` wraps `unittest.mock` and undoes every patch at test end: no decorators, no `with` nesting.

```python
def test_sends_email(mocker):
    send = mocker.patch("app.orders.send_email", autospec=True)      # patch where used
    place_order(user_id=1)
    send.assert_called_once_with(to="a@b.test", template="order_placed")

def test_uses_clock(mocker):
    mocker.patch.object(app.clock, "now", return_value=datetime(2024, 1, 1))
    mocker.patch.dict("os.environ", {"FEATURE_X": "1"})
```

## spy: real call + recording
```python
def test_cache_hits(mocker):
    spy = mocker.spy(repo, "load")
    svc.get(1); svc.get(1)
    assert spy.call_count == 1          # second call served from cache
    assert spy.spy_return.id == 1       # actual returned value
```
`spy_exception` holds a raised exception; works for async functions too.

## stub: callbacks
```python
cb = mocker.stub(name="on_done")
run(job, on_done=cb)
cb.assert_called_once()
```

## Async
`mocker.AsyncMock` (alias for `unittest.mock.AsyncMock`). Plain `mocker.patch` on an `async def` returns an `AsyncMock`; with `autospec=True` it returns an async function that mimics the signature (checked: not an `AsyncMock` instance, but `inspect.iscoroutinefunction` is true).

## Assertions with good diffs
Ordinary `unittest.mock` assertions work: `assert_has_calls([call(1), call(2)], any_order=False)`. The ini option `mock_use_standalone_module` switches to the PyPI `mock` package instead of `unittest.mock`.

## Gotchas
- `autospec=True` catches wrong signatures (calling with a non-existent kwarg fails), the main protection against mocks drifting from real code.
- `mocker.patch` returns the mock; using it as a context manager is not needed and emits a `PytestMockWarning`.
- `mocker.resetall()` resets call history mid-test; `mocker.stopall()` undoes patches early.

## Verify
Rename a parameter in the real function: the autospecced mock-based test fails.
