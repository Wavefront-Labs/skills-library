---
id: computing-software.software-engineering.crystal.annotations-in-macros
name: annotations-in-macros
category: computing-software
field: software-engineering
product: crystal
tags: [annotations-in-macros, annotations, annotation-macro, code-generation, serializable, reflection, instance-vars, field-annotation, crystal]
level: advanced
status: docs-checked
description: "Build annotation-driven features in Crystal with macros, in the way JSON::Serializable does."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/annotations/README.md
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/hooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotation-driven code generation

Goal: build annotation-driven features.

- Pattern: annotate instance variables, iterate `@type.instance_vars` inside a method-level macro, and read `ivar.annotation(MyAnn)`.
- `JSON::Serializable` and `YAML::Serializable` are the standard library examples of annotations that decide whether and under which key an ivar is serialized. An ORM can likewise mark a property as a column and keep column metadata (nullable, name, primary key) in the annotation; the ivar's name and type come from its `MetaVar`.
- Use `{% ann = ivar.annotation(MyAnn) %}` then `ann[:name]` (named fields) or `ann[0]` (positional).
- Hooks: `inherited` runs when a subclass is defined (`@type` is the subclass), `included` when a module is included, `finished` once parsing is done so all types and methods are known.

Gotchas:
- Annotations on method parameters are read through `@def.args[i].annotation(T)`; the block parameter through `@def.block_arg`.
- `TypeNode.instance_vars` currently only works inside an instance or class method.
- Annotations can only be read off typed block parameters.

Verify: define a toy `@[Column("n")]` and print columns at compile time.

## Checked
Checked 2026-11-02 against the crystal-book Annotations and Macro hooks pages. Removed: the specific `JSON::Field` option list (`key`, `ignore`, `converter`, `emit_null`; the API docs were not read), "compile time only" and macro-loop cost remarks.

Method: documentation only; no commands were run.
