---
id: computing-software.software-engineering.elixir.design-anti-patterns-boolean-obsession
name: design-anti-patterns-boolean-obsession
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, anti-pattern, boolean-obsession, exceptions-for-control-flow, unrelated-multi-clause, alternative-return-types, propagating-invalid-data, design-anti-patterns]
level: advanced
status: docs-checked
description: "Avoid exceptions for control flow, boolean obsession, functions with alternative return types and unrelated multi-clause functions, using the official fixes."
sources: ["https://hexdocs.pm/elixir/design-anti-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Design-related anti-patterns

**Goal:** design function APIs that are predictable, following the Elixir anti-patterns guide.

```elixir
# Boolean obsession: overlapping boolean options -> one option with atoms
def process(invoice, options \\ []) do
  case Keyword.get(options, :role, :default) do
    :admin -> ...
    :editor -> ...
    :default -> ...
  end
end

# Exceptions for control flow: use File.read/1 and case, not try/rescue around File.read!/1
case File.read(file) do
  {:ok, body} -> IO.puts(body)
  {:error, reason} -> IO.puts(:stderr, "could not read: #{inspect(reason)}")
end

# Alternative return types: one function per return type, not an option that changes it
parse(string)               # {integer, rest} | :error
parse_discard_rest(string)  # integer | :error
```

## Rules
- Documented design smells: alternative return types, boolean obsession, exceptions for control flow, primitive obsession, unrelated multi-clause function, using application configuration for libraries.
- Boolean obsession is a special case of primitive obsession: replace several booleans with overlapping states (`editor: true`, `admin: true`) by atoms (or a composite value).
- Prefer `case` and pattern matching over `try/rescue` to change the flow of code; use the tuple-returning function where one exists.
- Options that drastically change the return type make the result hard to predict: add a specific function for each return type.
- Primitive obsession: if you keep extracting parts of a string (for example an address), parse it once into a struct or map.
- Unrelated multi-clause function: clauses of one function should share one purpose; do not group unrelated business logic (and a `@doc` full of conditionals) in one definition.
- Libraries: the global application environment is shared by every user of the library; take configuration as function arguments or options instead.

## Self-check
Pick a function with a boolean flag argument and replace it with an atom option or two functions.

## Checked
Date: 2026-11-02. Confirmed against design-anti-patterns (smell list, boolean obsession role example, File.read refactor, alternative return types, primitive obsession, unrelated clauses, library config). Removed: fetch/fetch! pairing advice, String.split example, `use` hiding dependencies.
Method: documentation only; no commands were run.
