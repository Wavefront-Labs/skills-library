---
id: computing-software.software-engineering.crystal.macro-hooks-finished
name: macro-hooks-finished
category: computing-software
field: software-engineering
product: crystal
tags: [macro-hooks-finished, macros, macro-hooks, inherited, included, extended, method-added, finished, method-missing, crystal]
level: advanced
status: docs-checked
description: "Crystal macro hooks inherited, included, extended, method_added, method_missing and finished: when each runs, scope, stacking versus overriding."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/hooks.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/macros.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro hooks: inherited, included, method_added, finished

Goal: automate registration and codegen.

- `macro inherited` runs when a subclass is defined; `@type` is the inheriting type.
- `macro included` / `macro extended` run when a module is included or extended; `@type` is the including or extending type.
- `macro method_added(method)` runs when a method is defined in the current scope (`method.name` is available).
- `macro method_missing(call)` runs when a method is not found (`call.name`, `call.args`).
- `macro finished` runs after parsing finished, so all types and their methods are known. `@type.all_subclasses` is a `TypeNode` method that returns all subclasses of a type.
- `method_missing` and `method_added` apply only to calls or methods in the class that defines the macro and its descendants (or the top level if defined outside a class).
- Stacking: `inherited`, `included`, `extended`, `method_added` and `finished` can be defined several times and all run, in order of definition. `method_missing` is overridden: only the last definition in a context runs.

Gotchas:
- A regular macro called mid-class (such as one printing `@type.methods`) sees only the methods defined so far; `finished` runs once the type is completely defined, including reopened definitions.
- Use `finished` for scanning all subclasses or methods.

Verify: a `macro finished` that prints `@type.methods.map &.name` lists methods added by a reopened class.

## Checked

2026-11-03. Confirmed against the Crystal book "Hooks" page (hook list and semantics, scope rule for `method_missing`/`method_added`, stacking list, overriding rule, `finished` example) and `Crystal::Macros` source (`TypeNode#all_subclasses`).
Removed: `method.args`, the "`@type` is nil at the top level" claim, the claim that the generated `method_missing` method exists only when a call site exists, and the "inherited runs before the subclass's methods are visible" wording (replaced with the documented `finished` behaviour).
Method: documentation only; no commands were run.
