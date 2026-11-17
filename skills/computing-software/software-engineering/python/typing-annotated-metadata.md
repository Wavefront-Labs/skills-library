---
id: computing-software.software-engineering.python.typing-annotated-metadata
name: typing-annotated-metadata
category: computing-software
field: software-engineering
product: python
tags: [python, py-typing-advanced, typing-annotated, annotated, metadata, pydantic, fastapi, pep-593]
level: practitioner
status: docs-checked
description: "Attach validation and framework metadata to types with typing.Annotated: reading it via get_type_hints(include_extras=True), reusable aliases and Pydantic/FastAPI usage."
sources: ["https://docs.python.org/3/library/typing.html#typing.Annotated", "https://peps.python.org/pep-0593/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# typing.Annotated metadata

`Annotated[T, meta1, meta2]` is `T` to type checkers; the extras are carried for runtime consumers.

```python
from typing import Annotated, get_type_hints, get_args

PositiveInt = Annotated[int, "gt=0"]            # reusable alias
class Gt:
    def __init__(self, n): self.n = n
Age = Annotated[int, Gt(0)]

def f(x: Age): ...
hints = get_type_hints(f, include_extras=True)   # keeps Annotated; default strips it
base, *meta = get_args(hints["x"])               # int, [<Gt>]
```

## Where it is used
- Validation and web frameworks (for example Pydantic and FastAPI) read the metadata at runtime; see their own documentation for the markers they accept.
- Your own libraries: a unit-conversion or DI marker read from signatures.

## Rules
- Metadata can be any object; the first argument must be a valid type. Nested `Annotated` flattens, with metadata ordered starting from the innermost.
- The order of the metadata is preserved and matters for equality checks; metadata should be hashable and comparable for equality.
- Consumers must ignore metadata they do not recognise, and type checkers treat the annotation as plain `T`.

## Gotchas
- `get_type_hints()` strips `Annotated` unless `include_extras=True`.
- Type checkers ignore the metadata, so runtime enforcement is up to the consuming library.

## Verify
- [ ] A test asserts `get_args(get_type_hints(f, include_extras=True)["x"])` returns the expected metadata.
- [ ] Type checker still treats the parameter as plain `int`.

## Checked

2026-11-08. Confirmed on the typing.Annotated documentation and PEP 593: `Annotated[T, x]` is treated as `T` by checkers, metadata order is preserved and matters for equality, nested `Annotated` is flattened innermost first, `get_type_hints(include_extras=...)` strips the extras unless True, unrecognised metadata must be ignored, and metadata must be hashable and comparable for equality. Removed: the Pydantic/FastAPI argument examples, the `ClassVar` ordering rule and the import-time and lazy-annotation remarks (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
