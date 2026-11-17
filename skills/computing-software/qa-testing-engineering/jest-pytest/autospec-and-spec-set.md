---
id: computing-software.qa-testing-engineering.jest-pytest.autospec-and-spec-set
name: autospec-and-spec-set
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [autospec, spec-set, unittest-mock, mocking, create-autospec]
level: practitioner
status: verified
description: "Keep Python mocks honest with autospec, spec and spec_set: signature checking, failing on misspelled attributes, create_autospec for classes, and the performance trade-off."
sources:
  - https://docs.python.org/3/library/unittest.mock.html#autospeccing
  - https://docs.python.org/3/library/unittest.mock.html#unittest.mock.create_autospec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autospec and spec_set to keep mocks honest

**Problem:** a plain `Mock` accepts any call and any attribute. Tests pass even when the real API changed or a method name is misspelled (`mock.assert_called_once_wiht()` used to silently pass before Python 3.5 added protection for `assert*` typos).

## Levels of strictness
| Option | Effect |
|---|---|
| `Mock()` | anything goes |
| `Mock(spec=Real)` | only attributes that exist on `Real` can be read; setting new attributes allowed |
| `Mock(spec_set=Real)` | reading and setting unknown attributes raises AttributeError |
| `create_autospec(Real)` / `patch(..., autospec=True)` | spec applied recursively; methods check call signatures |

## Examples
```python
from unittest.mock import patch, create_autospec

def test_sends_receipt():
    with patch("shop.checkout.EmailClient", autospec=True) as Client:
        checkout(order)
        client = Client.return_value
        client.send.assert_called_once_with(to="ada@example.test", template="receipt")
        # client.send(to=..., tmpl=...) would raise TypeError: wrong signature

gateway = create_autospec(PaymentGateway, instance=True, spec_set=True)
gateway.charge.return_value = ChargeResult(ok=True)
gateway.chrage(...)   # AttributeError: Mock object has no attribute 'chrage'
```
pytest-mock: `mocker.patch("shop.checkout.EmailClient", autospec=True)`, `mocker.create_autospec(...)`.

## Instance attributes set in __init__
Autospec sees class attributes only; attributes created in `__init__` are missing. (checked: `create_autospec(Cls, instance=True).conn` raises AttributeError; `create_autospec(Cls())` on a real instance has it.) Options: declare them at class level (type annotations with defaults), set them on the mock explicitly, or use `spec_set` on a real instance (`create_autospec(real_instance)`).

## Async
Autospec of `async def` methods produces `AsyncMock` automatically (3.8+): `await client.fetch()` works and `assert_awaited_once_with` is available.

## Trade-offs
Autospec introspects the target and is slower to create; cache it in fixtures for heavy classes. It can execute descriptors/properties during introspection (confirmed: `create_autospec(PaymentGateway())` on a real instance ran a property getter; autospeccing the class did not).

## Gotchas
- `return_value` of an autospecced class is the instance mock; configure methods there.
- Autospeccing a function preserves its signature check, but a `side_effect` function's own signature is not compared with the spec: it receives the call's arguments, so a mismatch only surfaces as a `TypeError` raised from inside the call (checked on Python 3.14).

## Verify
Renaming a method or changing its parameters in production code makes the mocked tests fail.
