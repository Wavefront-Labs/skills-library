---
id: computing-software.software-engineering.elixir.quote-unquote-defmacro
name: quote-unquote-defmacro
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, quote, unquote, defmacro, ast, hygiene, macro-expand, quote-macros, elixir-metaprogramming]
level: advanced
status: docs-checked
description: "Inspect the AST with quote, write hygienic macros with defmacro, and prefer functions unless you need compile-time code."
sources: ["https://hexdocs.pm/elixir/macros.html", "https://hexdocs.pm/elixir/Kernel.SpecialForms.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# quote, unquote and macros

**Goal:** understand the three-tuple AST and write a minimal macro correctly.

```elixir
quote do: sum(1, 2, 3)   #=> {:sum, [], [1, 2, 3]}
Macro.to_string(quote do: a + b)
Macro.expand_once(quote(do: unless(true, do: 1)), __ENV__)

defmodule My do
  defmacro unless_nil(expr, do: block) do
    quote do
      if unquote(expr) != nil, do: unquote(block)
    end
  end
end
# the call site needs `require My`
```

## Rules
- The building block of macros is a tuple with three elements: name, metadata and arguments.
- Macros are hygienic: variables defined inside a macro do not affect the user code; use `var!/1` deliberately to break hygiene. Macros are lexical, so callers must `require` or `import` the module.
- `unquote` injects values and `unquote_splicing` splices a list; `bind_quoted:` is recommended whenever you inject a value into the quote, and it disables `unquote`.
- Macros should only be used as a last resort; prefer functions and data structures.
- Debug with `Macro.to_string/1` and `Macro.expand_once/2`.

## Failure modes
- Injecting values with plain `unquote` inside a quote is error prone; the Kernel.SpecialForms docs recommend `bind_quoted` whenever a value is injected.

## Self-check
Quote a variable inside a module: its third element is the module atom, not `nil`, which marks its context and keeps it hygienic.

## Checked
2026-11-03: confirmed against the Elixir macros guide and Kernel.SpecialForms docs (three-element AST tuples, hygiene and `var!`, `require` for macros, `Macro.expand_once/2`, `Macro.to_string/1`, `bind_quoted`, `unquote_splicing`, last-resort advice, context atom on variables). Removed: the `quote` metadata output shown for `1 + 2`, the literals-quote-to-themselves list, the `apply` remark and `Macro.expand/2`.
Method: documentation only; no commands were run.
