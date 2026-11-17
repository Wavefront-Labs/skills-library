---
id: computing-software.software-engineering.software-architecture.interpreter-pattern
name: interpreter-pattern
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, design-patterns, behavioral-patterns, interpreter-pattern, dsl, abstract-syntax-tree]
level: advanced
status: verified
description: "Build small DSL interpreters with the Interpreter pattern: grammar, AST node classes with evaluate, parsing, and when to switch to a parser generator or compilation."
sources: ["https://refactoring.guru/design-patterns/interpreter", "https://craftinginterpreters.com/", "https://martinfowler.com/books/dsl.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreter

Represent a simple language's grammar as classes, one per rule, and evaluate sentences by
walking the resulting abstract syntax tree (AST).

## When it fits
Small, stable grammars evaluated many times: filter expressions (`status = "PAID" AND total > 100`),
pricing or eligibility rules, feature-flag targeting, search query syntax, template conditions.

## Structure
```python
class Expr(Protocol):
    def eval(self, ctx: dict) -> object: ...

import operator
OPS = {"=": operator.eq, ">": operator.gt, "<": operator.lt}   # looked up, not all evaluated

@dataclass
class Field:
    name: str
    def eval(self, c): return c.get(self.name)

@dataclass
class Lit:
    value: object
    def eval(self, c): return self.value

@dataclass
class Cmp:
    op: str; l: Expr; r: Expr
    def eval(self, c):
        a, b = self.l.eval(c), self.r.eval(c)
        if self.op != "=" and (a is None or b is None): return False   # missing field
        return OPS[self.op](a, b)        # str vs int with ">" still raises TypeError: type-check the AST first

@dataclass
class And:
    l: Expr; r: Expr
    def eval(self, c): return self.l.eval(c) and self.r.eval(c)
```
(Run: `status = "PAID" AND total > 100` gives True, then False for a missing `total`, and False for another status. The earlier version put `def` after `;` on the class line, a SyntaxError, and built a dict that evaluated every operator before indexing it, so `=` on a str and an int raised TypeError.)
Pair with a parser: a hand-written recursive-descent parser for one grammar rule per function is
fine for small languages (Crafting Interpreters, part II). Grammar first in EBNF:
```
expr   := term ("OR" term)* ;  term := factor ("AND" factor)* ;
factor := "NOT" factor | "(" expr ")" | cmp ;  cmp := IDENT OP literal
```

## Rules
- Separate parsing (text -> AST) from evaluation; validate the AST (known fields, type checks) once
  before evaluating many times.
- Never `eval()` user input in the host language as a shortcut; that's code injection.
- Bound evaluation (depth, node count, time) when users write expressions.
- Multiple operations over the AST (eval, pretty-print, compile to SQL) -> Visitor pattern instead
  of methods on each node.

## Outgrowing it
Grammar grows or performance matters: use a parser generator (ANTLR, Lark, tree-sitter), compile to
bytecode/closures, or embed an existing expression language (CEL, JSONLogic, Lua) rather than
growing your own.
