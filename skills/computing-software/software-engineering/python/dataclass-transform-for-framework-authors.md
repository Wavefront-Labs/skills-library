---
id: computing-software.software-engineering.python.dataclass-transform-for-framework-authors
name: dataclass-transform-for-framework-authors
category: computing-software
field: software-engineering
product: python
tags: [python, py-annotations, dataclass-transform, pep-681, orm-models, type-checking, framework-authoring]
level: advanced
status: docs-checked
description: "Tell type checkers that your decorator, base class or metaclass synthesises a dataclass-style __init__, using @dataclass_transform (PEP 681, Python 3.11)."
sources: ["https://docs.python.org/3/library/typing.html#typing.dataclass_transform", "https://peps.python.org/pep-0681/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dataclass_transform for framework authors

If your library builds `__init__` from annotations (ORMs, validators, attrs-likes), type checkers cannot see it. `@typing.dataclass_transform()` (3.11) declares dataclass-like semantics.

```python
from typing import dataclass_transform, Any

def field(*, default: Any = ..., kw_only: bool = False) -> Any: ...

@dataclass_transform(kw_only_default=True, field_specifiers=(field,))
class ModelMeta(type): ...

class Model(metaclass=ModelMeta): ...

class User(Model):
    id: int
    name: str = field(default="anon")

User(id=1)                 # checker synthesises __init__(*, id: int, name: str = ...)
User(1)                    # error: keyword-only
```

## Three attachment points
- A **decorator** function (`@my_dataclass`), a **base class** (`__init_subclass__`), or a **metaclass** (as above).
- Options mirror dataclass behaviour: `eq_default`, `order_default`, `frozen_default`, `kw_only_default`, plus `field_specifiers` (functions/classes that declare per-field options such as `init=False`, `default`, `default_factory`, `alias`).

## Rules
- Your runtime must really implement what you declare; the decorator performs no runtime work.
- Supported field specifier parameters: `init`, `default`, `default_factory`, `factory`, `kw_only`, `alias`.
- Subclasses of a transformed class are assumed to behave like stdlib dataclasses, including inheritance and field overrides as in PEP 557.

## Gotchas
- A subclass of a `Model` subclass inherits the transform; attributes on the decorated class or metaclass itself and on its base classes are not fields.
- `kw_only_default` defaults to False and `field_specifiers` to an empty tuple, so name your field functions explicitly.

## Verify
- [ ] A `reveal_type(User.__init__)` or call-error test file in the repo checked by your type checker in CI.
- [ ] Positive and negative call examples (missing required field, wrong type) produce expected diagnostics.

## Checked

2026-11-08. Confirmed on the typing.dataclass_transform documentation and PEP 681: the decorator applies to a function, class or metaclass, added in 3.11, parameters `eq_default` (default True), `order_default`, `kw_only_default` (default False), `frozen_default` and `field_specifiers` (default empty), field specifier parameters `init`, `default`, `default_factory`, `factory` (an alias for `default_factory`), `kw_only` and `alias`, subclass inheritance behaving like stdlib dataclasses. Removed: the `typing_extensions` remark, the MRO ordering rule, the claim of differing pyright and mypy completeness and the `**kwargs` bullet (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
