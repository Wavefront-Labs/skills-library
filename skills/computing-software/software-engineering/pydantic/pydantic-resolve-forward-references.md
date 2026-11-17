---
id: computing-software.software-engineering.pydantic.pydantic-resolve-forward-references
name: pydantic-resolve-forward-references
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-forward-annotations, model-rebuild, forward-reference, recursive-models, cyclic-imports, type-checking]
level: practitioner
status: docs-checked
description: "Fix not fully defined Pydantic models: forward annotations, self-referencing models, model_rebuild and cyclic imports across modules."
sources:
  - https://docs.pydantic.dev/latest/concepts/forward_annotations/
  - https://docs.pydantic.dev/latest/concepts/models/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reference types that are not defined yet (later in the file, itself, or another module).

Python 3.14 and later: annotations are not eagerly evaluated, so you can reference undefined names directly (`sibling: Foo | None = None` inside `Foo`).

Python 3.13 and lower: quote the annotation or add `from __future__ import annotations`:

```python
from __future__ import annotations

class Model(BaseModel):
    a: MyInt

MyInt = int
print(Model(a='1'))  #> a=1
```

Self-referencing models: annotations are resolved during model creation; before 3.14 write `sibling: 'Foo | None' = None`.

model_rebuild(): if an annotation names something undefined at class creation, using the model raises `PydanticUserError`: "`Foo` is not fully defined; you should define `Bar`, then call `Foo.model_rebuild()`." (error code class-not-fully-defined). Define `Bar`, then call `Foo.model_rebuild()`. Call it proactively for recursive models or generics. Rebuilding the outermost model builds the core schema for the whole tree, so all types at all levels must be ready first.

Cyclic imports (two modules whose models reference each other):
- Python 3.15: use `lazy from .b import B` (lazy imports) in each module.
- Python 3.14 and lower: in `a.py` import `B` only under `if TYPE_CHECKING:` and annotate `b: 'B | None' = None`; `b.py` imports `A` normally. `B` is not available at runtime in `a.py`, so `A` stays incomplete. In a parent module (for example `__init__.py`) import both and call `A.model_rebuild()`:

```python
from .a import A
from .b import B
A.model_rebuild()
```

Cyclic data (not types): validating input that contains a reference cycle gives a `ValidationError` with type `recursion_loop`, not a `RecursionError`.

For a `TypeAdapter` with forward refs, see the TypeAdapter rebuild skill.

## Checked

Checked 2026-11-07. Re-read concepts/forward_annotations and concepts/models in full and compared every claim; no changes needed.

Method: documentation only; no commands were run.
