---
id: computing-software.software-engineering.python.unittest-mock-patching-and-autospec
name: unittest-mock-patching-and-autospec
category: computing-software
field: software-engineering
product: python
tags: [python, py-unit-testing, unittest-mock, mock, magicmock, patch, autospec, create-autospec, side-effect, assert-called]
level: practitioner
status: docs-checked
description: "Replace collaborators with unittest.mock: patch where the name is looked up, autospec to catch signature drift, side_effect sequences and exceptions, call assertions."
sources: ["https://docs.python.org/3/library/unittest.mock.html", "https://docs.python.org/3/library/unittest.mock.html#where-to-patch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# unittest.mock: patching and autospec

```python
from unittest import mock

# Patch the name where it is LOOKED UP (the module under test), not where it is defined
with mock.patch("myapp.billing.requests.post", autospec=True) as post:
    post.return_value.status_code = 201
    post.return_value.json.return_value = {"id": 7}
    result = myapp.billing.charge(100)
post.assert_called_once_with("https://pay/api", json={"amount": 100}, timeout=5)

@mock.patch("myapp.service.time.sleep")               # decorators inject mocks bottom-up
def test_retries(sleep): ...

m = mock.Mock(side_effect=[TimeoutError, {"ok": True}])   # first call raises, second returns
m(); 
mock.patch.object(Client, "fetch", return_value=b"x")
mock.patch.dict(os.environ, {"MODE": "test"}, clear=False)   # restores after the block
```

## Why autospec
A plain `Mock` accepts any call: `post.assert_called_once_with(...)` passes with misspelled attributes, and `mock.nonexistent_method()` silently works. `autospec=True` (or `create_autospec(cls, instance=True)`) copies the real signature and attributes, so wrong arguments raise `TypeError` and missing attributes raise `AttributeError`. Use `spec_set=True` to also forbid setting unknown attributes.

## Assertions
`assert_called_with`, `assert_called_once_with`, `assert_any_call`, `assert_has_calls([...], any_order=False)`, `call_args.kwargs`, `call_count`, `mock_calls`, `reset_mock()`. Async: `AsyncMock` and `patch` auto-detects `async def` targets (3.8+); assert with `assert_awaited_once_with`.

## Gotchas
- Wrong patch target is the #1 bug: with `from requests import post` in `myapp.billing`, patch `myapp.billing.post`.
- With the default `unsafe=False`, accessing an attribute whose name starts with `assert`, `assret`, `asert`, `aseert` or `assrt` raises `AttributeError`, which catches misspelled assertions; other made-up names (such as `called_once_with`) still just create a child mock.
- `assert_called_with` and `assert_called_once_with` only check the most recent call; `assert_any_call` passes if the mock was ever called with those arguments.
- `reset_mock()` does not clear `return_value`, `side_effect` or attributes you set by assignment unless you pass the keyword arguments.
- Over-mocking couples tests to implementation; prefer fakes for storage/clock and mock only the boundary (network, time, randomness).
- `MagicMock` is a `Mock` subclass with all the magic methods pre-created; use `Mock` when you do not need them.

## Verify
- [ ] Break the production signature on purpose and confirm the autospecced test fails.
- [ ] No test depends on call order unless it asserts `mock_calls`.

## Checked
2026-11-09. Confirmed against the Python 3 unittest.mock docs (patch where the name is looked up, bottom-up decorator order, side_effect iterables and exceptions, spec/spec_set/unsafe, create_autospec instance=True, assert_* methods, reset_mock, AsyncMock auto-selection since 3.8, MagicMock). Removed the "mutable args recorded by reference" note, the `called_once_with` silent-pass claim, and the MagicMock truthiness remark. Autospec signature errors (`TypeError`) are shown in the docs example. The page was searched for each claim, not read end to end.
Method: documentation only; no commands were run.
