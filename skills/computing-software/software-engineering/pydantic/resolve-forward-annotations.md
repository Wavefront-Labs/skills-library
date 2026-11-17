---
id: computing-software.software-engineering.pydantic.resolve-forward-annotations
name: resolve-forward-annotations
category: computing-software
field: software-engineering
product: pydantic
tags: [pydantic, pydantic-annotation-resolution, forward-reference, model-rebuild, class-not-fully-defined, undefined-annotation, namespace, postponed-annotations]
level: advanced
status: docs-checked
description: "Fix class-not-fully-defined and undefined-annotation in Pydantic, and understand how forward references are resolved at class creation and with model_rebuild."
sources:
  - https://docs.pydantic.dev/latest/internals/resolving_annotations/
  - https://docs.pydantic.dev/latest/errors/usage_errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Forward references and model rebuilds

Goal: get a model with string or not-yet-defined annotations fully built.

## The errors

- `class-not-fully-defined` (`PydanticUserError`): a type in an annotation is not defined yet, e.g. `a: Optional['Bar'] = None` used before `Bar` exists. Fix: define the type, then call `Foo.model_rebuild()`. Usage works once both classes exist.
- `undefined-annotation` (`PydanticUndefinedAnnotation`): raised from `Model.model_rebuild()` when an annotation like `'B'` still cannot be resolved.
- `unevaluable-type-annotation`: annotations are evaluated after assignments, so `date: date = Field(...)` in a class clashes. Use `import datetime` and `date: datetime.date`, or `from datetime import date as _date`.

## How resolution works at class creation

Pydantic roughly follows `typing.get_type_hints()`, using `eval()` with globals and locals. For each base in the MRO (reverse order, starting with the root base):

1. Read `__annotations__` from the base's `__dict__`.
2. Evaluate each annotation. Globals are the module `__dict__`. Locals, highest priority first: `{cls.__name__: cls}` (recursion support), the class's own `__dict__`, then the parent namespace (frame locals if defined inside a function).
3. If evaluation fails, the annotation is kept as is so the model can be rebuilt later. A failed model has a `MockCoreSchema` as `__pydantic_core_schema__`.

## Limitations

- `cls.__dict__` may include irrelevant names, so `f: '__doc__'` unexpectedly resolves.
- For models defined in a function, a copy of the frame locals at definition time is kept (weak references, to avoid memory leaks). Later local names are missing, even on a later rebuild. Function locals apply to models only, not dataclasses, TypedDicts or named tuples.
- During schema generation of a nested dataclass, the parent namespace, the rebuild namespace and `{Bar.__name__: Bar}` are added at lowest priority, so `Foo` with `a: 'Bar | None'` and `Bar(BaseModel)` with `b: Foo` works without `model_rebuild()`. This can create inconsistencies, e.g. `__pydantic_complete__` being True when it should be False.

## `model_rebuild()` namespace

Pass `_types_namespace` explicitly, or the caller's namespace is used. It merges with the model's parent namespace. Example failure: a model defined in `func()` with `f: 'A | Forward'`, rebuilt outside with `_types_namespace={'Forward': str}`, raises `PydanticUndefinedAnnotation: name 'A' is not defined`.

Background: `from __future__ import annotations` stringifies annotations (PEP 563). The page hopes PEP 649 (Python 3.14) will simplify this; v2.10 refactored the logic.

## Checked

Checked 2026-11-07. Re-read internals/resolving_annotations in full. For errors/usage_errors, read only the Class not fully defined, Undefined annotation and Cannot evaluate type annotation sections, not the whole page. Compared every claim; no changes needed.

Method: documentation only; no commands were run.
