---
id: computing-software.software-engineering.python.positional-only-and-keyword-only-parameters
name: positional-only-and-keyword-only-parameters
category: computing-software
field: software-engineering
product: python
tags: [python, py-functions, positional-only-keyword-only, pep-570, pep-3102, api-design, signatures]
level: practitioner
status: docs-checked
description: "Use / and * in signatures (PEP 570, PEP 3102) to lock call styles, keep parameter names out of the public API and evolve signatures without breaking callers."
sources: ["https://docs.python.org/3/tutorial/controlflow.html#special-parameters", "https://peps.python.org/pep-0570/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Positional-only and keyword-only parameters

```python
def connect(host, port=5432, /, *, timeout=10.0, ssl=True): ...
#           ^^^^^^^^^^^^^^^^   ^   ^^^^^^^^^^^^^^^^^^^^^^
#           positional-only    |   keyword-only
connect("db", 5433, timeout=3)        # ok
connect(host="db")                    # TypeError: positional-only passed by keyword
connect("db", 5432, 3)                # TypeError: timeout must be a keyword
```
Parameters between `/` and `*` may be positional-or-keyword. `/` is Python 3.8+ (PEP 570).

## When to use which
The tutorial's guidance:
- **Positional-only** when parameter names have no real meaning, when you want to enforce argument order, or when you need positional parameters plus arbitrary keywords: `def foo(name, /, **kwds)` lets `kwds` contain a `name` key without ambiguity.
- **Keyword-only** when names have meaning and the definition is clearer with explicit names, or to stop users relying on position.
- For an API, use positional-only to prevent breaking changes if a parameter's name changes later.

## Evolving a signature
Add new options only as keyword-only with defaults; callers never break. To change a
positional parameter, accept both for a release and emit `DeprecationWarning`.

## Gotchas
- Keyword-only without defaults must still be given: `def f(*, a)` requires `f(a=1)`.
- In dataclasses use `field(kw_only=True)` or `@dataclass(kw_only=True)` (3.10+).
- `inspect.signature` reports each parameter's kind (positional-only, positional-or-keyword, keyword-only).

## Verify
- [ ] `inspect.signature(f)` prints `/` and `*` where intended.
- [ ] Tests assert the `TypeError` for the forbidden call style so the contract stays.

## Checked

- 2026-11-03: checked against the CPython docs `tutorial/controlflow.rst` (special parameters, positional-only guidance, `**kwds` example), `library/dataclasses.rst` (`kw_only`), `library/inspect.rst` (parameter kinds) and PEP 570 (Python 3.8).
- Removed: the `__name` double-underscore convention claim and the `functools.partial`/C-function `inspect.signature` claim. The "Evolving a signature" section is general practice advice, not documented behaviour.

Method: documentation only; no commands were run.
