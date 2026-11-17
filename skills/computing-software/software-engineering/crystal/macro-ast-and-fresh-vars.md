---
id: computing-software.software-engineering.crystal.macro-ast-and-fresh-vars
name: macro-ast-and-fresh-vars
category: computing-software
field: software-engineering
product: crystal
tags: [macro-ast-and-fresh-vars, macros, ast-nodes, fresh-variable, macro-run, typenode, macro-methods, compile-time-execution, read-file, crystal]
level: advanced
status: docs-checked
description: "Crystal macros: AST node types, fresh variables with %name, read_file and run at compile time, @type, @top_level, env and raise."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/fresh_variables.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/macros.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AST nodes, fresh variables and run

Goal: write hygienic and powerful macros.

- Node types include `ArrayLiteral`, `HashLiteral`, `StringLiteral`, `NumberLiteral`, `Call`, `Def`, `TypeNode`, `MacroId`, `Var` and `Nop`. Test with `{{ x.is_a?(NumberLiteral) }}` and read the name with `x.class_name`.
- Macro-generated local variables are visible in the caller (a macro with `x = 1` overwrites the caller's `x`). Declare `%x = 1` for a fresh variable that cannot clash with local variables in scope.
- `%name{key1, key2}` declares a fresh variable keyed on other nodes, for example `%name{index}` inside a `{% for name, index in names %}` loop; the same key gives the same variable.
- `{{ read_file("path") }}` embeds a file's contents at compile time; relative paths resolve against the current working directory, so use `"#{__DIR__}/file.txt"` to read relative to the source file. `read_file?` returns `nil` on I/O failure.
- `{{ run("./gen.cr", args) }}` compiles and executes a Crystal program and returns its output as a `MacroId`.
- `@type.instance_vars`, `@type.methods`, `@type.name`, `@def` and `@top_level` are available inside macros.
- `{% raise "message" %}` aborts compilation with a custom error. `{{ env("VAR") }}` reads an environment variable at compile time (`nil` if unset).

Gotchas:
- Macros work on the AST at compile time, not on runtime values; `env` reads the environment of the compiler run.
- `run` is discouraged for slow programs or ones that change between compilations (the compiler may cache the executable for the file).
- Opening an HTTP connection inside a `run` program is called out as likely to slow compilation badly.

Verify: print the expansion with `{% debug %}`.

## Checked

2026-11-03. Confirmed against the Crystal book "Fresh variables" and "Macros" pages and `Crystal::Macros` source (`read_file`, `read_file?`, `run`, `env`, `raise`, `class_name`, `__crystal_pseudo_is_a?`, `TypeNode#instance_vars/methods`).
Fixed: `read_file` paths were claimed relative to the compiling file; they resolve against the working directory. Removed: the "keep macro bodies short" and "heavy run slows incremental builds" advice (docs only warn about slow or changing run programs), `%tmp{i}` spelling in favour of the documented `%name{key}` form.
Method: documentation only; no commands were run.
