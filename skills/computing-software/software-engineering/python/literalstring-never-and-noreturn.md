---
id: computing-software.software-engineering.python.literalstring-never-and-noreturn
name: literalstring-never-and-noreturn
category: computing-software
field: software-engineering
product: python
tags: [python, py-typing-advanced, literalstring-never, literalstring, never, noreturn, assert-never, sql-injection]
level: practitioner
status: docs-checked
description: "Use LiteralString to type-check injection-prone APIs, and Never/NoReturn for functions that cannot return and for exhaustiveness checks."
sources: ["https://typing.python.org/en/latest/spec/special-types.html#never-and-noreturn", "https://peps.python.org/pep-0675/", "https://docs.python.org/3/library/typing.html#typing.assert_never"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LiteralString, Never and NoReturn

## LiteralString (3.11+, PEP 675)
Accepts only strings the checker knows are literals, or built from literals. Use it on sinks where untrusted text is dangerous:
```python
from typing import LiteralString

def run_sql(query: LiteralString, params: tuple = ()) -> list: ...

run_sql("SELECT * FROM t WHERE id = ?", (uid,))     # ok
run_sql(f"SELECT * FROM t WHERE name = '{name}'")   # error: name is a plain str
```
Concatenating two `LiteralString` values stays `LiteralString`; an f-string or `s.format(...)` is `LiteralString` only if its constituent expressions (and `s`) are. `LiteralString` is a special form for type checking only: nothing is enforced at runtime.

## NoReturn and Never (Never: 3.11+)
```python
from typing import NoReturn, Never, assert_never

def fail(msg: str) -> NoReturn:          # always raises or exits
    raise SystemExit(msg)

def handle(x: int | str) -> str:
    if isinstance(x, int): return "i"
    elif isinstance(x, str): return "s"
    else: assert_never(x)                # error if a union member is unhandled
```
`Never` (3.11+) is the bottom type and is equivalent to `NoReturn`; by convention `NoReturn` annotates function returns and `Never` is used elsewhere. Checkers treat code after a `NoReturn` call as unreachable.

## Gotchas
- A `NoReturn` function that can return (even implicitly, returning `None`) is flagged by type checkers.
- A `Literal["a","b"]` is assignable to `LiteralString`, not vice versa; `LiteralString` is assignable to `str`.

## Verify
- [ ] Run a type checker on a snippet passing a non-literal f-string and confirm the error appears.
- [ ] Add an enum member and confirm the `assert_never` branch fails type checking.

## Checked

2026-11-08. Confirmed on the typing specification (Special types: NoReturn and Never) and PEP 675: `NoReturn` annotates functions that never return and implicit `None` return is an error, code after such calls is unreachable, `Never` since Python 3.11 is the bottom type equivalent to and interchangeable with `NoReturn`, `LiteralString` sits between `Literal[...]` and `str`, concatenation, f-string and `.format` rules, and it is used solely for type checking. Removed: the `AssertionError` runtime claim for `assert_never`, `cast` defeating the guard, the mypy/pyright wording and the library-overload advice (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
