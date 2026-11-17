---
id: computing-software.software-engineering.python.repr-str-and-format-protocols
name: repr-str-and-format-protocols
category: computing-software
field: software-engineering
product: python
tags: [python, py-data-model, dunder-repr-str-format, repr, str, format-spec, dunder-methods]
level: practitioner
status: docs-checked
description: "Implement __repr__, __str__ and __format__ so objects print usefully in logs and f-strings, with expression-style reprs and custom format specs."
sources: ["https://docs.python.org/3/reference/datamodel.html#object.__repr__", "https://docs.python.org/3/reference/datamodel.html#object.__format__"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# repr, str and format protocols

**Goal:** every class has an unambiguous `repr` for developers, an optional readable `str`
for users, and a `__format__` only when a format spec means something.

## Rules
- `__repr__` is the fallback for everything: containers, logs, debugger, `!r`. Aim for
  `ClassName(field=value)` that could be pasted back into code; if not possible use
  `<ClassName id=7 state=open>`.
- `__str__` falls back to `__repr__`; define it only if a human-facing form differs.
- `format(obj, spec)` and f-strings call `type(obj).__format__(obj, spec)`. The default
  `object.__format__` raises `TypeError` for a non-empty spec.

```python
class Money:
    def __init__(self, cents, cur="EUR"): self.cents, self.cur = cents, cur
    def __repr__(self): return f"{type(self).__name__}({self.cents!r}, {self.cur!r})"
    def __str__(self): return f"{self.cents/100:.2f} {self.cur}"
    def __format__(self, spec):
        if spec == "short": return f"{self.cents/100:.0f}{self.cur}"
        return format(str(self), spec)      # delegate everything else to str

m = Money(1250)
assert f"{m}" == "12.50 EUR" and f"{m:short}" == "12EUR" and f"{m!r}" == "Money(1250, 'EUR')"
```

## Gotchas
- Keep `__repr__` simple: it should be an information-rich, unambiguous representation, ideally a valid Python expression, otherwise `<...>`.
- Recursive structures: use `reprlib.recursive_repr()` as a decorator to avoid infinite recursion.
- Large containers: `reprlib.Repr` truncates; do not dump 1M items into a log line.
- `__repr__` must return a string object.
- Dataclasses generate `__repr__` for you (`repr=False` per field hides secrets such as tokens).

## Verify
- [ ] `eval(repr(obj)) == obj` for value-like classes (a unit test), or the repr is clearly angle-bracketed.
- [ ] Secrets are excluded from `repr`.
- [ ] `f"{obj:badspec}"` raises a clear error, not silently wrong output.

## Checked

- 2026-11-03: checked against the CPython docs `reference/datamodel.rst` (`__repr__`, `__str__`, `__format__`, default `object.__format__` TypeError for a non-empty spec since 3.4), `library/reprlib.rst` (`recursive_repr`, `Repr`) and `library/dataclasses.rst` (`field(repr=False)`).
- Removed: the claims that debuggers and tracebacks call `__repr__` on broken objects and that returning bytes or None raises `TypeError`; `__bytes__` dropped from the description (not covered in the body).

Method: documentation only; no commands were run.
