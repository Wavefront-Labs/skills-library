---
id: computing-software.software-engineering.python.ast-parsing-and-nodetransformer
name: ast-parsing-and-nodetransformer
category: computing-software
field: software-engineering
product: python
tags: [python, py-introspection, ast-node-transformer, ast, nodevisitor, nodetransformer, code-analysis, codemod, ast-unparse]
level: advanced
status: docs-checked
description: "Analyse and rewrite Python source with ast: parse, NodeVisitor, NodeTransformer, fix_missing_locations, ast.unparse and the limits of unparsing and parsing untrusted input."
sources: ["https://docs.python.org/3/library/ast.html", "https://docs.python.org/3/library/ast.html#ast.NodeTransformer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ast parsing and NodeTransformer

```python
import ast

src = open("mod.py", encoding="utf-8").read()
tree = ast.parse(src, filename="mod.py")
print(ast.dump(tree, indent=4))                     # inspect node shapes while you write the visitor

class FindPrints(ast.NodeVisitor):                  # read-only analysis
    def __init__(self):
        self.hits = []
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.hits.append(node.lineno)
        self.generic_visit(node)                    # otherwise children of this node are not visited

v = FindPrints(); v.visit(tree); print(v.hits)

class Rename(ast.NodeTransformer):                  # rewrite
    def visit_Name(self, node):
        if node.id == "old":
            return ast.copy_location(ast.Name(id="new", ctx=node.ctx), node)
        return node                                  # None removes the node; for statements a list may be returned

new_tree = ast.fix_missing_locations(Rename().visit(tree))
print(ast.unparse(new_tree))                         # added in 3.9
code = compile(new_tree, "mod.py", "exec")
```

## Rules from the docs
- `ast.parse(source, filename, mode='exec', type_comments=False, ...)`: `mode='eval'` parses one expression, `mode='single'` a single interactive statement, `mode='func_type'` signature type comments. With `type_comments=True` type comments are returned (and misplaced ones are syntax errors).
- `NodeVisitor.visit` calls `visit_<ClassName>` or `generic_visit`; child nodes of a node with a custom visitor are visited only if the method calls `generic_visit()` or visits them itself. `NodeTransformer` uses the return value: `None` removes the node, otherwise it replaces it (the original node means no change).
- If a transformer adds nodes without location information, call `ast.fix_missing_locations()` on the new subtree; `ast.copy_location(new, old)` copies it from an old node.
- `lineno` is 1-indexed; `col_offset` is the byte offset in the UTF-8 string the parser uses; end positions are optional.
- Other helpers: `ast.walk`, `ast.iter_child_nodes`, `ast.get_docstring`, `ast.get_source_segment(source, node)`.
- `ast.Constant` is the literal node. `ast.Num`, `ast.Str`, `ast.Bytes`, `ast.NameConstant` and `ast.Ellipsis` were deprecated in 3.8 and removed in 3.14.
- Python 3.14 adds `TemplateStr` and `Interpolation` nodes for t-strings.

## Gotchas
- `ast.unparse` output is not necessarily equal to the original code, so formatting is not preserved; unparsing a highly complex expression raises `RecursionError`.
- A sufficiently large or complex string can crash the interpreter in `ast.parse` because of stack-depth limits; cap input size for untrusted input.
- Parsing is not a safety check: do not `compile` or `exec` untrusted code. `ast.literal_eval` accepts only literals but is documented as not free from denial-of-service (memory or C stack exhaustion).
- In 3.13 creating nodes with missing required fields is deprecated (removal planned in 3.15), so pass every field.

## Verify
- [ ] A test per supported Python version covers any new syntax the tool must accept.

## Checked
Date: 2026-11-03. Confirmed against the `ast` module documentation: parse modes and parameters, NodeVisitor/NodeTransformer behaviour, `fix_missing_locations`, `copy_location`, `col_offset` bytes, removed node classes, t-string nodes, `unparse` warnings, stack-depth crash warning, `literal_eval` warning. Removed as unconfirmed: libcst, ruff/flake8/rope/bowler recommendations, `symtable`/`tokenize` advice, "unsafe to modify during walk", round-trip dump test, file-size cap number.
Method: documentation only; no commands were run.
