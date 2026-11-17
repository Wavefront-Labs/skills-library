---
id: computing-software.software-engineering.crystal.macro-basics
name: macro-basics
category: computing-software
field: software-engineering
product: crystal
tags: [macro-basics, macros, macro, macro-interpolation, macro-if, macro-for, compile-time, expand, crystal]
level: practitioner
status: docs-checked
description: "Define Crystal macros with macro, paste AST with {{ }}, branch and loop with {% %}, use .id, variadic args, @type, and debug with {% debug %}."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/macros/README.md
  - https://github.com/crystal-lang/crystal/blob/master/src/compiler/crystal/macros.cr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro basics: macro, {{ }} and {% %}

Goal: write simple macros.

```crystal
macro define_method(name, content)
  def {{name.id}}
    {{content}}
  end
end

define_method :foo, 1
foo # => 1
```
- A macro receives AST nodes at compile time and produces code that is pasted into the program. The generated code must itself be valid Crystal (no lone `when`, no `def` without `end`).
- `{{ ... }}` pastes (interpolates) a node as-is; `{% ... %}` runs code without output (`if`, `for`, assignment).
- Without `.id`, a symbol argument is pasted as `:foo`, giving the invalid `def :foo`. `.id` turns a node into an identifier.
- Conditionals: `{% if cond %} ... {% elsif %} ... {% else %} ... {% end %}`. `Nop`, `NilLiteral` and a false `BoolLiteral` are falsey; everything else is truthy.
- Loops: `{% for i in (1..count) %}`, `{% for name, index in array_literal %}`, `{% for key, value in hash_literal %}`; usable inside and outside macro definitions.
- Variadic: `macro m(*names)` packs arguments into a `TupleLiteral`; `{{*values}}` pastes the elements comma-separated.
- `@type` is the `TypeNode` of the current scope (always the instance type, even in a class method); `@top_level`, `@def` and `@caller` also exist.
- Macro methods on nodes include `.id`, `.stringify`, `.symbolize`, `.camelcase`, `.underscore`, `.size` and `.map` (on the node types that define them; see `Crystal::Macros`).
- Compile-time checks: `{% if flag?(:x86_64) %}` tests a compile-time flag.
- Debug: `{% debug %}` prints the macro's generated code at compile time (the formatter is applied unless you pass `false`).

Gotchas:
- Macro expressions are evaluated even inside comments, so a macro cannot be commented out with `#`.
- To generate a whole `case`, wrap it in `{% begin %} ... {% end %}` so `case` is inside the macro.
- A nested macro needs `\{% ... %}` escapes (or `verbatim do ... end`) so the outer macro does not evaluate them.

Verify: `{% debug %}` shows the expansion at build time.

## Checked

2026-11-03. Confirmed against the Crystal book "Macros" page (interpolation, `.id`, conditionals and falsey values, iteration, variadic and splat, `@type`, `@top_level`, `@def`, `@caller`, comments, pitfalls, nested macros, verbatim) and `Crystal::Macros` source (`debug`, `flag?`, `symbolize`, `camelcase`, `underscore`, `size`, `map`).
Removed: the `crystal tool expand ... --cursor` form (the tool takes `-c`/`--cursor LOC` before the file, see tool-implementations-unreachable), the claim that macros expand before type checking, the `{{ yield }}` claim, `p!` as a macro debugger, and the unsupported "define_getter" ivar example.
Method: documentation only; no commands were run.
