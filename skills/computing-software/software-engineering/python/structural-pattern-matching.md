---
id: computing-software.software-engineering.python.structural-pattern-matching
name: structural-pattern-matching
category: computing-software
field: software-engineering
product: python
tags: [python, python-data-model, structural-pattern-matching, match-statement, match-args, pep-634]
level: practitioner
status: verified
description: "Use match/case for parsing commands, ASTs and JSON-like data: literal, capture, class, mapping and sequence patterns, guards, __match_args__ and the capture trap."
sources:
  - https://peps.python.org/pep-0636/
  - https://peps.python.org/pep-0634/
  - https://docs.python.org/3/reference/compound_stmts.html#the-match-statement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structural pattern matching (match/case)

**Goal:** replace nested isinstance/key checks with declarative patterns, without falling into the name-capture trap.

## 1. Pattern kinds
```python
match event:
    case {"type": "click", "pos": [x, y]}:                 # mapping + sequence; extra keys allowed
        handle_click(x, y)
    case {"type": "key", "key": str(k)} if k.isprintable(): # class pattern for type check + guard
        handle_key(k)
    case {"type": "resize", **rest}:
        handle_resize(rest)
    case _:
        log.warning("unknown event %r", event)
```
- Literals: numbers, strings, `None`, `True`, `False` (compared by `==`, singletons by `is`).
- Sequence: `[first, *rest]`, `(a, b)`; matches lists/tuples but **not** str/bytes.
- Mapping: matches keys present; `**rest` captures the remainder.
- OR: `case 401 | 403:`; AS: `case [Point() as p, *_]:`.

## 2. Class patterns and __match_args__
```python
@dataclass
class Point:
    x: int
    y: int

match shape:
    case Point(x=0, y=0): print("origin")
    case Point(0, y):    print(f"on y axis at {y}")       # positional uses __match_args__
    case Circle(center=Point(x, y), r=r) if r > 10: ...
```
Dataclasses and NamedTuples set `__match_args__` automatically; plain classes need `__match_args__ = ("x", "y")` for positional patterns.

## 3. The capture trap
```python
RED = "red"
match color:
    case RED:         # WRONG: binds a new variable named RED, matches anything
        ...
```
Only **dotted names** are value patterns: use `Color.RED` (an Enum) or `case c if c == RED`. CPython raises `SyntaxError: name capture 'RED' makes remaining patterns unreachable` when more cases follow; a lone `case RED:` silently matches everything (ruff only hinted at an unused variable and pyright and mypy were silent, so test for it).

## 4. Good fits
- Command parsing: `match cmd.split(): case ["go", direction]: ... case ["quit" | "exit"]: ...`
- AST/visitor-like dispatch on node types.
- Versioned payloads: `case {"version": 2, "data": {...}}`.
Poor fit: simple value switches (a dict lookup is clearer) or type dispatch better done with polymorphism / `functools.singledispatch`.

## Gotchas
- Patterns are checked top to bottom; put specific cases before general ones. A bare capture or `_` before other cases is a `SyntaxError` ("wildcard makes remaining patterns unreachable").
- Mapping patterns ignore extra keys; to forbid them, capture `**rest` and guard `if not rest`.
- Exhaustiveness: pyright/mypy can check `assert_never(x)` in `case _:` for enums and unions.
- Requires Python 3.10+.

## Verify
- Unit tests feed one payload per case plus an unknown payload; a type checker run reports no unreachable/irrefutable pattern warnings.

## Checked
- Python 3.14.0: ran all patterns: mapping with extra keys, sequence patterns reject `str`/`bytes`, OR, AS, guards, `**rest`; `__match_args__` is set for dataclasses and NamedTuples and a plain class without it raised `TypeError: Plain() accepts 0 positional sub-patterns (2 given)`; the capture trap (lone `case RED:` matched `'blue'`, followed by other cases it is a `SyntaxError`; so is a wildcard before other cases); `Color.RED` value pattern; command parsing. ruff, pyright and mypy were run on the capture and did not flag it.
