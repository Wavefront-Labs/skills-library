---
id: computing-software.software-engineering.python.deferred-annotations-with-annotationlib
name: deferred-annotations-with-annotationlib
category: computing-software
field: software-engineering
product: python
tags: [python, py-annotations, annotationlib-deferred, pep-649, pep-749, python-314, forward-references, annotationlib]
level: practitioner
status: docs-checked
description: "Python 3.14 evaluates annotations lazily (PEP 649/749): use annotationlib.get_annotations with Format.VALUE, FORWARDREF or STRING and know the three execution models."
sources: ["https://docs.python.org/3/library/annotationlib.html", "https://docs.python.org/3/whatsnew/3.14.html#pep-649-749-deferred-evaluation-of-annotations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deferred annotations (Python 3.14+)

## Execution models (annotationlib docs)
- Stock semantics, default in 3.0 through 3.13: annotations evaluated eagerly where they appear.
- Stringified annotations, with `from __future__ import annotations` (3.7+): stored as strings only.
- Deferred evaluation, default in 3.14 and newer (PEP 649, PEP 749): annotations are stored in special-purpose annotate functions (`__annotate__`) and evaluated lazily, only when accessed. The future import still keeps stringified behaviour.

```python
import annotationlib
from annotationlib import Format

def func(arg: Undefined): ...

annotationlib.get_annotations(func, format=Format.VALUE)       # NameError: Undefined is not defined
annotationlib.get_annotations(func, format=Format.FORWARDREF)  # {'arg': ForwardRef('Undefined', owner=...)}
annotationlib.get_annotations(func, format=Format.STRING)      # {'arg': 'Undefined'}
```

## Which format
- `VALUE` (the default): real values; may raise `NameError` for names that cannot be resolved. For `VALUE`, `__annotations__` is tried first, then `__annotate__`.
- `FORWARDREF = 3`: real values for defined names and `ForwardRef` proxies for undefined ones; good for inspecting without evaluating.
- `STRING = 4`: the annotation text as in the source, up to modifications such as whitespace normalisation; the exact strings may change in future Python versions. Useful for documentation generators.
- `ForwardRef` has an `evaluate()` method taking `owner`, `globals`, `locals` and `type_params` to supply bindings; with no scope information it uses empty globals and locals.
- Helpers: `annotations_to_string()`, `call_annotate_function()`, `call_evaluate_function()` and `get_annotate_from_class_namespace()` (for metaclasses before the class exists).

## Migration
- The What's New porting section lists the changes that may be needed; in most cases code keeps working as-is.
- Metaclass code that runs during class creation should not touch `__annotations__` blindly; use `get_annotate_from_class_namespace()` to obtain the annotate function from the namespace.

## Verify
- [ ] A test calls `get_annotations(..., format=Format.FORWARDREF)` on a function with an undefined name and gets a `ForwardRef`.

## Checked
Date: 2026-11-03. Confirmed against the `annotationlib` documentation and the What's New 3.14 section on PEP 649/749 (execution models, formats, `ForwardRef.evaluate`, helper functions, the example outputs). Removed as unconfirmed: `typing.get_type_hints` comparisons, advice on removing the future import, `cls.__dict__["__annotations__"]` breakage, dataclass/Pydantic remarks, CI matrix advice, the `Node | None` example.
Method: documentation only; no commands were run.
