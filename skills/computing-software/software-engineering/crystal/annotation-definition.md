---
id: computing-software.software-engineering.crystal.annotation-definition
name: annotation-definition
category: computing-software
field: software-engineering
product: crystal
tags: [annotation-definition, annotations, annotation, custom-annotation, annotation-args, macro-annotation, ann-method, metadata, crystal]
level: advanced
status: docs-checked
description: "Define and read custom annotations in Crystal macros."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/annotations/README.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining and reading annotations

Goal: attach compile-time metadata.

```crystal
annotation Route; end
class Ctl
  @[Route(path: "/x", method: "GET")]
  def x; end
  macro finished
    {% for m in @type.methods %}
      {% if a = m.annotation(Route) %}
        puts {{ a[:path] }}
      {% end %}
    {% end %}
  end
end
```
- Declare with `annotation Name; end`. Apply to instance and class methods, instance variables, classes, structs, enums, modules, and method parameters.
- Fields are key/value (`@[Ann(key: "v")]`) or positional (`@[Ann("foo", 123)]`).
- Read from a `TypeNode`, `Def`, `MetaVar` or `Arg` with `.annotation(T)`. Key/value: `a[:name]` (Symbol, String or MacroId) and `a.named_args` (a NamedTupleLiteral; `.double_splat` passes them on). Positional: `a[0]` (one index at a time; a missing index is `nil`) and `a.args` (a TupleLiteral).
- `.annotations` returns all annotations on the node; `.annotations(T)` only those of type `T`.
- Annotations on ivars: iterate `@type.instance_vars` and call `ivar.annotation(T)`. Parameters: `@def.args[0].annotation(T)`, `@def.block_arg.annotation(T)`.

Gotchas:
- If the same annotation is applied more than once, `.annotation(T)` returns the last one; use `.annotations(T)` for all.
- `finished` runs once the type is fully defined (including re-opened classes), so all methods are known.
- `TypeNode.instance_vars` currently only works inside an instance or class method.
- Annotations can only be read off typed block parameters.

Verify: the macro output prints when building.

## Checked
Checked 2026-11-02 against the crystal-book Annotations and Macro hooks pages. Confirmed everything above. Removed: runtime-availability remark, the unknown-annotation compile error claim.

Method: documentation only; no commands were run.
