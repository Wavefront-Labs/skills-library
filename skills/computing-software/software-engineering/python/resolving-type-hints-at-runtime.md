---
id: computing-software.software-engineering.python.resolving-type-hints-at-runtime
name: resolving-type-hints-at-runtime
category: computing-software
field: software-engineering
product: python
tags: [python, py-annotations, get-type-hints-runtime, get-type-hints, get-origin, get-args, forward-references, introspection]
level: practitioner
status: docs-checked
description: "Introspect annotations safely at runtime with typing.get_type_hints, get_origin, get_args and is_typeddict, handling forward refs, unions, Optional and Annotated."
sources: ["https://docs.python.org/3/library/typing.html#typing.get_type_hints", "https://docs.python.org/3/library/typing.html#typing.get_origin"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resolving type hints at runtime

Raw `__annotations__` may hold strings or `ForwardRef` objects. `typing.get_type_hints` resolves them:

```python
from typing import get_type_hints, get_origin, get_args, Union
import types

class User:
    id: int
    tags: list[str]
    parent: "User | None"

hints = get_type_hints(User)                          # evaluates string annotations
get_origin(hints["tags"]), get_args(hints["tags"])    # (list, (str,))
get_origin(hints["parent"]) in (Union, types.UnionType)   # works on old and new Pythons

def unwrap_optional(tp):
    if get_origin(tp) in (Union, types.UnionType):
        args = [a for a in get_args(tp) if a is not type(None)]
        return args[0] if len(args) == 1 else tp
    return tp
```

## `get_type_hints(obj, globalns=None, localns=None, include_extras=False, *, format=Format.VALUE)`
- Evaluates string or `ForwardRef` annotations in `globalns`, `localns` and the object's type-parameter namespace; if namespaces are not given they are inferred from `obj`.
- Replaces `None` with `types.NoneType`.
- For a class, merges annotations along `C.__mro__`; earlier classes in the MRO take precedence.
- Strips `Annotated[T, ...]`, `Required[T]`, `NotRequired[T]` and `ReadOnly[T]` down to `T` **unless `include_extras=True`** (the default is `False`).
- Since 3.11 an annotation with a `None` default is returned unchanged (older versions added `Optional[t]` for functions and methods).
- `format` was added in 3.14; see `annotationlib.get_annotations()`.
- It may execute arbitrary code contained in annotations (see the docs' security note). With `Format.VALUE`, unresolved forward references, for example names imported only under `if TYPE_CHECKING:`, raise `NameError`; invalid annotation code can raise any exception.
- Calling it on an instance is unsupported (and since 3.14 no longer accepted); use `get_type_hints(type(obj))`.

## `get_origin` and `get_args`
- `get_origin(Dict[str, int])` is `dict` (typing aliases are normalised); `get_origin(str)` is `None`; `get_origin(Annotated[str, "m"])` is `Annotated`.
- `get_args(Dict[int, str])` is `(int, str)`; `get_args(int)` is `()`. For unions and `Literal` nested in another generic, argument order may differ from the original because of type caching.
- Since 3.14 `types.UnionType` is an alias for `Union`, so `Union[int, str]` and `int | str` are the same class: use `isinstance(obj, Union)`, or for older versions `get_origin(obj) is Union or get_origin(obj) is types.UnionType`.
- `typing.is_typeddict(tp)` tests for a `TypedDict` class.

## Verify
- [ ] Unit test the resolver on `int | None`, `Optional[int]`, `Annotated[int, x]` and a forward-reference class.
- [ ] A class with a `TYPE_CHECKING`-only import is handled by catching `NameError`, not by crashing the tool.

## Checked
Date: 2026-11-03. Confirmed against the typing module docs for `get_type_hints`, `get_origin`, `get_args`, `is_typeddict`, `Optional` and the 3.14 `Union` change. Fixed a real error: `include_extras` defaults to `False`, not `True`. Removed as unconfirmed: the `Callable` nested-shape example, `isinstance(x, list[int])` claim, `localns` advice for function-local classes, comparison remark on `typing.List`.
Method: documentation only; no commands were run.
