---
id: computing-software.software-engineering.python.closures-nonlocal-and-late-binding
name: closures-nonlocal-and-late-binding
category: computing-software
field: software-engineering
product: python
tags: [python, py-functions, closures-nonlocal, nonlocal, late-binding, scoping, legb, free-variables]
level: practitioner
status: docs-checked
description: "Understand LEGB scoping, closures, nonlocal and global, and fix the late-binding loop-variable bug in lambdas and callbacks."
sources: ["https://docs.python.org/3/reference/executionmodel.html#resolution-of-names", "https://docs.python.org/3/reference/simple_stmts.html#the-nonlocal-statement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures, nonlocal and late binding

A name is resolved using the nearest enclosing scope: local, then enclosing functions, then global (module), then the builtins namespace. If a name is bound anywhere in a code block, all uses of it in that block refer to the local one.

```python
def counter():
    n = 0
    def inc():
        nonlocal n          # rebinding an enclosing variable needs nonlocal
        n += 1
        return n
    return inc

c = counter(); assert (c(), c()) == (1, 2)
```
Without `nonlocal`, `n += 1` raises `UnboundLocalError` (a subclass of `NameError`): `n` is local and used before it is bound.
`nonlocal` binds to the nearest enclosing function binding and is a `SyntaxError` if no such binding exists; `global` does the same for module names. Rebinding needs the declaration; `items.append(x)` does not rebind.

## Late binding
The FAQ explains that a lambda's free variable is looked up when the lambda is called, not when it is defined, and that this applies to regular functions too:
```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]                    # [2, 2, 2]
fs = [lambda i=i: i for i in range(3)]       # default arg evaluated at definition time
[f() for f in fs]                    # [0, 1, 2]
```

## Inspecting
`fn.__closure__` is a tuple of cells for the function's free variables (named in `fn.__code__.co_freevars`); each cell has a `cell_contents` attribute.

## Gotchas
- The scope of names defined in a class block does not extend to methods, comprehensions or generator expressions inside it (annotation scopes can see them): `b = list(a + i for i in range(10))` fails in a class body where `a = 42`.
- `nonlocal` must come before the name is used or assigned in that scope, or a `SyntaxError` is raised.

## Verify
- [ ] A test builds several closures in a loop and asserts distinct results.
- [ ] Callbacks created in loops bind the loop value explicitly (default argument).

## Checked

- 2026-11-03: checked against the CPython docs `reference/executionmodel.rst` (resolution of names, `UnboundLocalError`, class block scope), `reference/simple_stmts.rst` (`nonlocal`), `reference/datamodel.rst` (`__closure__`, `co_freevars`, `cell_contents`) and `faq/programming.rst` (UnboundLocalError and lambdas-in-a-loop entries).
- Removed: the LEGB name, the 3.12 inlined-comprehension remark, the `functools.partial` fix, the memory-leak claim, the threads/async remark, the `global` smell opinion and the pyflakes/ruff `B023` check.

Method: documentation only; no commands were run.
