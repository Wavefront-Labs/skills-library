---
id: computing-software.software-engineering.python.introspection-with-inspect-signature
name: introspection-with-inspect-signature
category: computing-software
field: software-engineering
product: python
tags: [python, py-introspection, inspect-signature, inspect, signature, bind, getmembers, getsource, dependency-injection]
level: practitioner
status: docs-checked
description: "Introspect callables and objects with inspect: Signature and bind for validation and DI, getmembers, getsource, iscoroutinefunction and unwrapping decorated functions."
sources: ["https://docs.python.org/3/library/inspect.html", "https://docs.python.org/3/library/inspect.html#introspecting-callables-with-the-signature-object"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Introspection with inspect.signature

```python
import inspect

def handler(request, user_id: int, *, verbose: bool = False) -> str: ...

sig = inspect.signature(handler)
for name, p in sig.parameters.items():
    print(name, p.kind.name, p.annotation, p.default is inspect.Parameter.empty)
# request POSITIONAL_OR_KEYWORD ... ; verbose KEYWORD_ONLY ...
sig.return_annotation                       # <class 'str'>

bound = sig.bind(req, 7, verbose=True)      # TypeError if args do not fit: validate callbacks and plugins early
bound.apply_defaults(); bound.arguments     # {'request': req, 'user_id': 7, 'verbose': True}

def call_with(fn, **available):             # dependency injection: pass only what fn asks for
    wanted = inspect.signature(fn).parameters
    return fn(**{k: v for k, v in available.items() if k in wanted})
```

## Other tools
```python
inspect.getmembers(obj, inspect.isfunction)     # sorted (name, value) pairs; predicate filters
inspect.iscoroutinefunction(fn)                 # async def; partial objects supported since 3.8
inspect.isgeneratorfunction(fn); inspect.isclass(x); inspect.isabstract(cls)
inspect.getsource(fn); inspect.getsourcefile(fn); inspect.getdoc(fn)    # OSError if the source cannot be retrieved; TypeError for built-in module/class/function
inspect.unwrap(decorated)                       # follows __wrapped__ to the original function
inspect.get_annotations(fn, eval_str=True)      # added 3.10; alias of annotationlib.get_annotations in 3.14
inspect.stack()[1].function                     # caller name; delete frame references when done (reference cycles)
inspect.currentframe(); inspect.getattr_static(obj, "x")   # attribute without triggering descriptors/__getattr__
```

## Gotchas
- `signature()` raises `ValueError` if no signature can be provided and `TypeError` if the object type is unsupported; wrap in `try/except (ValueError, TypeError)` for arbitrary callables.
- `signature()` follows `__wrapped__` chains by default (`follow_wrapped=True`), so decorators using `functools.wraps` expose the original signature.
- `eval_str=True` can execute arbitrary code: the docs warn against using it on untrusted input.
- Frame objects can create reference cycles; the docs advise deleting the reference (`del frame`) when done.

## Verify
- [ ] Unit test the DI helper with positional-only, keyword-only and `**kwargs` targets.
- [ ] `signature(decorated)` equals `signature(original)` when `wraps` is used.

## Checked

- 2026-11-03: checked against the CPython docs `library/inspect.rst` (`signature`, `Signature.bind`, `Parameter` kinds, `getmembers`, `getsource` errors, `unwrap`, `get_annotations` 3.10 and 3.14 note, `iscoroutinefunction` 3.8, `getattr_static`, frame reference-cycle note).
- Removed: the claims that `signature(cls)` reflects `__init__`, that partial keyword-fixed parameters become keyword-only, and that `stack()` is slow.

Method: documentation only; no commands were run.
