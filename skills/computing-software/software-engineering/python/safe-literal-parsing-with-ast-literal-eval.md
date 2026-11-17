---
id: computing-software.software-engineering.python.safe-literal-parsing-with-ast-literal-eval
name: safe-literal-parsing-with-ast-literal-eval
category: computing-software
field: software-engineering
product: python
tags: [python, py-security, ast-literal-eval, literal-eval, eval-exec-danger, config-parsing, expression-evaluator, simpleeval]
level: practitioner
status: docs-checked
description: "Parse Python literals from strings with ast.literal_eval instead of eval, know its limits (DoS, no operators), and build safe calculators with ast walking."
sources: ["https://docs.python.org/3/library/ast.html#ast.literal_eval"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Safe literal parsing with ast.literal_eval

`eval` and `exec` execute arbitrary code, so never use them on untrusted input. `ast.literal_eval` is specifically designed not to execute Python code: no namespace, no name lookups, no calls.

```python
import ast

ast.literal_eval("{'a': [1, 2.5, None], 'b': (True, 'x')}")    # dicts, lists, tuples, sets, str, bytes, numbers, None, bool, Ellipsis
ast.literal_eval("__import__('os')")                             # raises (a call is not a literal)
ast.literal_eval("1 + 2")                                        # raises (operators are not supported)
```
Typical uses: reading a repr'd dict from a log/config file or round-tripping `repr()` of simple data. Prefer JSON/TOML for formats you design.

## Limits
- The docs say it is not free from attack: a relatively small input can exhaust memory or the C stack and crash the process, and some inputs cause excessive CPU use. Calling it on untrusted data is not recommended. If you must, cap input length and catch `ValueError`, `TypeError`, `SyntaxError`, `MemoryError` and `RecursionError`.
- It cannot evaluate names, calls, indexing or operators.

## A small safe calculator by walking the AST
```python
import ast, operator as op
OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.USub: op.neg}

def calc(expr: str):
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](ev(n.operand))
        raise ValueError(f"disallowed: {ast.dump(n)[:40]}")
    return ev(ast.parse(expr, mode="eval").body)
calc("2 * (3 + 4) ** 2")        # 98 -- note: Pow can be abused ("9**9**9"): bound exponents or drop Pow
```

## Gotchas
- Since 3.10 leading spaces and tabs are stripped from string input; since 3.9 `'set()'` creates an empty set.

## Verify
- [ ] Fuzz or table-test with `__import__`, attribute access, lambda, a 1 MB nested list; each is rejected quickly.
- [ ] No `eval`/`exec` is applied to external data.

## Checked

- 2026-11-03: checked against the CPython docs `library/ast.rst` (`literal_eval` and its warnings, `ast.parse` modes, `Constant`, `BinOp`, `UnaryOp`, `Pow`, `USub`).
- Removed: eval sandbox-escape specifics, complex/unary literal claim, exact error message, simpleeval, argparse use, pickle/yaml/pandas comparisons, ruff rule, and the `functions.html#eval` source (not readable in this batch).

Method: documentation only; no commands were run.
