---
id: computing-software.software-engineering.python.typeddict-literal-and-namedtuple
name: typeddict-literal-and-namedtuple
category: computing-software
field: software-engineering
product: python
tags: [python, python-typing, typeddict, typing-literal, namedtuple, notrequired, required, readonly, json-typing, enum]
level: practitioner
status: verified
description: "Type dict-shaped data and fixed choices: TypedDict with Required/NotRequired/ReadOnly, Literal unions, NamedTuple, and when to use a dataclass instead."
sources: ["https://typing.python.org/en/latest/spec/typeddict.html", "https://peps.python.org/pep-0655/", "https://peps.python.org/pep-0705/", "https://docs.python.org/3/library/typing.html#typing.Literal"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypedDict, Literal and NamedTuple

**Goal:** give precise types to JSON payloads, config dicts and string-valued options,
which are where untyped Python bugs hide.

## TypedDict for dict-shaped data you don't own
```python
from typing import TypedDict, NotRequired, Required, ReadOnly, Literal

class User(TypedDict):
    id: int
    email: str
    nickname: NotRequired[str]          # key may be absent (PEP 655)

class Patch(TypedDict, total=False):    # all optional...
    id: Required[int]                   # ...except this one
    email: str

class Event(TypedDict):
    kind: ReadOnly[Literal["created", "deleted"]]   # PEP 705, 3.13+ / typing_extensions
```
- TypedDict is a plain `dict` at runtime: no validation, no defaults. Validate untrusted
  input with pydantic or a schema library.
- `NotRequired` means the key can be MISSING, not that the value can be `None`.
  For nullable: `nickname: str | None`.
- Access optional keys with `.get()`; pyright flags `user["nickname"]` (`reportTypedDictNotRequiredAccess`); mypy did not.
- Extra keys: TypedDicts are structural and allow extra keys from subtypes, so
  iterating `.items()` gives `object` values.

## Literal for fixed choices
```python
Mode = Literal["r", "w", "a"]
def open_log(mode: Mode) -> None: ...
open_log("x")   # type error
```
Literal unions narrow with `==`/`in` and work great as discriminators:
`if event["kind"] == "created": ...`. Use `enum.Enum`/`StrEnum` instead when you need
iteration over members, methods, or runtime validation.

## NamedTuple
```python
class Point(NamedTuple):
    x: float
    y: float = 0.0
```
Immutable, indexable, unpackable, cheap. Good for return values of a few fields.
Downside: it IS a tuple, so `Point(1, 2) == (1, 2)` is True and positional order is API.

## Which one?
| Data | Choose |
|---|---|
| External JSON / kwargs dicts you pass through | TypedDict |
| Your own domain objects with behaviour or defaults | `@dataclass` (slots, frozen) |
| Small immutable record, tuple semantics wanted | NamedTuple |
| Validated input at a boundary | pydantic model |

## Verify
- [ ] Payload tests include a missing optional key and a wrong literal value; the checker flags the misuse.
- [ ] No `dict[str, Any]` remains on public function signatures where a TypedDict fits.

## Checked
- mypy 2.4.0 and pyright 1.1.414 on Python 3.14.0: missing required keys (`typeddict-item`), `NotRequired`/`Required` with `total=False`, `ReadOnly` mutation error, `nickname=None` rejected for `NotRequired[str]`, `.items()` values reveal `object`; pyright flagged indexing a `NotRequired` key and mypy did not; `Literal` argument "x" rejected and `==` narrowing revealed `Literal['created']`; at runtime a TypedDict is a plain `dict` and accepts a wrong value; `NamedTuple` equals a plain tuple. `typing.ReadOnly` imports on 3.14; the 3.13 introduction was not re-read.
