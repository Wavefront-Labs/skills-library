---
id: computing-software.software-engineering.python.argument-binding-and-star-args
name: argument-binding-and-star-args
category: computing-software
field: software-engineering
product: python
tags: [python, py-functions, argument-binding-star-args, args, kwargs, unpacking, mutable-defaults]
level: practitioner
status: docs-checked
description: "How Python binds positional, keyword, default and *args/**kwargs arguments, call-site unpacking, mutable default traps and forwarding wrappers correctly."
sources: ["https://docs.python.org/3/reference/compound_stmts.html#function-definitions", "https://docs.python.org/3/reference/expressions.html#calls"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argument binding and star-args

## Binding order
Parameters are filled: positionals left to right, then keywords by name, then defaults;
leftovers go to `*args` (tuple) and `**kwargs` (dict). A keyword that matches no parameter (without `**kwargs`) or a duplicate value raises `TypeError`.

```python
def f(a, b=2, *args, c, d=4, **kw): ...
f(1, 2, 3, 4, c=5, z=9)   # a=1 b=2 args=(3,4) c=5 d=4 kw={'z': 9}

opts = {"c": 1}
f(*[1, 2], **opts)         # call-site unpacking
```

## Defaults are evaluated once
```python
def add(x, bucket=[]):            # BUG: one list shared by every call
    bucket.append(x); return bucket

def add(x, bucket=None):          # fix: sentinel
    bucket = [] if bucket is None else bucket
```
Use a private `_MISSING = object()` sentinel when `None` is a legal value.

## Forwarding wrappers
```python
import functools
def logged(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        print(fn.__name__, args, kwargs)
        return fn(*args, **kwargs)
    return wrapper
```

## Gotchas
- `**kwargs` hides typos; for public APIs list keyword-only parameters explicitly.
- `**mapping` at a call site must be a mapping whose keys are strings, and no key may repeat a parameter already given (`TypeError: f() got multiple values for keyword argument 'a'`).

## Verify
- [ ] A test calls the function twice and asserts no state leaks through defaults.
- [ ] A call with a duplicate keyword raises `TypeError` in a test.

## Checked

2026-11-08. Confirmed on the Python reference pages (Calls; Function definitions): slot-filling of positionals then keywords, excess positionals go to `*identifier` as a tuple and excess keywords to `**identifier` as a dict, an unmatched keyword raises `TypeError` unless `**identifier` exists, default values are evaluated once when the function is defined (mutable-default warning), `**expression` must be a mapping with string keys and a repeated parameter raises `TypeError` with the `got multiple values for keyword argument 'a'` message. Removed: late-binding lambda claim, `{**a, **b}` merge-order remark, `args` reassignment bullet and the `inspect.signature` check (not on the cited pages).

Method: docs-only read of cited pages, 2026-11-08
