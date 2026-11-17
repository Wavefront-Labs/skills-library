---
id: computing-software.software-engineering.python.exception-groups-and-chaining
name: exception-groups-and-chaining
category: computing-software
field: software-engineering
product: python
tags: [python, exception-groups, python-exception-chaining, except-star, add-note, raise-from, custom-exceptions]
level: practitioner
status: verified
description: "Design and handle Python exceptions well: custom hierarchies, raise from vs implicit chaining, add_note, ExceptionGroup and except*, and not swallowing errors."
sources: ["https://docs.python.org/3/tutorial/errors.html", "https://docs.python.org/3/library/exceptions.html#exception-groups", "https://peps.python.org/pep-0654/", "https://peps.python.org/pep-0678/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Exception groups and chaining

**Goal:** errors that carry their cause and context, are catchable at the right
granularity, and survive concurrency (several failures at once).

## A library exception hierarchy
```python
class PaymentError(Exception):
    """Base for everything this package raises."""
class CardDeclined(PaymentError):
    def __init__(self, code: str):
        super().__init__(f"card declined: {code}")
        self.code = code
class GatewayUnavailable(PaymentError): ...
```
Callers catch `PaymentError` broadly or a subclass precisely. Subclass `Exception`, never
`BaseException` (that is for `KeyboardInterrupt`, `SystemExit`, `CancelledError`).

## Chaining
```python
try:
    resp = client.post(...)
except httpx.TimeoutException as e:
    raise GatewayUnavailable("gateway timed out") from e     # explicit: __cause__
```
- `raise X from e`: traceback says "The above exception was the direct cause...".
- Raising inside `except` without `from`: implicit `__context__`, "During handling of the
  above exception, another exception occurred" - usually signals a bug in the handler.
- `raise X from None` suppresses the context when the original is noise (e.g. KeyError
  translated to a domain error).

## Notes (3.11+)
```python
except ValueError as e:
    e.add_note(f"while parsing row {lineno} of {path}")
    raise
```
Adds context without changing type; shown at the end of the traceback.

## ExceptionGroup and except* (3.11+)
Raised by `asyncio.TaskGroup`, `trio`, and anything that runs several things concurrently.
```python
try:
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch(a)); tg.create_task(fetch(b))
except* TimeoutError as eg:          # eg is an ExceptionGroup of just the TimeoutErrors
    log.warning("timeouts: %d", len(eg.exceptions))
except* ValueError as eg:
    ...
```
- Each `except*` clause can run; unmatched exceptions re-raise as a (smaller) group.
- A plain `except TimeoutError` does NOT catch a group containing one; use `except*`
  or `except ExceptionGroup`.
- Raise your own: `raise ExceptionGroup("validation failed", errors)` to report all
  problems at once. `eg.subgroup(pred)` / `eg.split(pred)` filter.

## Anti-patterns
- `except Exception: pass` - at minimum log with `logger.exception(...)`.
- Bare `except:` catches `KeyboardInterrupt` and `SystemExit`.
- Catching to return `None`/sentinel: forces every caller to check; raise instead.
- `try` blocks wrapping 30 lines: keep the try body to the call that can fail.

## Verify
- [ ] Tracebacks in logs show "direct cause" chains for translated errors.
- [ ] Tests use `pytest.raises(CardDeclined, match="...")` and `pytest.RaisesGroup` / `except*` for groups.
## Checked
Run with Python 3.14.0 on Windows with pytest 9.1: `raise ... from e` gives `__cause__` and the direct-cause text; implicit chaining gives `During handling`; `from None` sets `__suppress_context__`; `add_note` appears at the end of the traceback and in `__notes__`; a TaskGroup with two TimeoutErrors and a ValueError is split by two `except*` clauses (groups of 2 and 1); plain `except TimeoutError` does not catch the group; an unmatched type re-raises as a smaller group; `split` and `subgroup`; `except* Exception` wraps in an ExceptionGroup; `pytest.RaisesGroup` exists in pytest 9.1 (not run in a test). Not run: Python 3.10 or older, trio.
Linux pass (Python 3.14.8 standalone musl build in a WSL2 busybox distro): every check above gave the same result as on Windows.
