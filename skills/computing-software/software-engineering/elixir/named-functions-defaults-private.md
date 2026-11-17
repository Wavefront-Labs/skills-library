---
id: computing-software.software-engineering.elixir.named-functions-defaults-private
name: named-functions-defaults-private
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, def, defp, default-arguments, function-head, arity, named-functions]
level: practitioner
status: docs-checked
description: "Define public and private functions, default arguments with function heads for multi-clause functions, and the arity-based naming rule."
sources: ["https://hexdocs.pm/elixir/modules-and-functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named functions, defaults and private functions

**Goal:** structure functions with clear arity, defaults and visibility, following the Elixir modules-and-functions guide.

```elixir
defmodule Math do
  def sum(a, b), do: do_sum(a, b)       # public: callable from other modules
  defp do_sum(a, b), do: a + b          # private: callable only inside the module

  def zero?(0), do: true                # several clauses; first matching clause runs
  def zero?(x) when is_integer(x), do: false
end

defmodule Concat do
  # a function head declares defaults once for a multi-clause function
  def join(a, b, sep \\ " ")
  def join(a, b, _sep) when b == "", do: a
  def join(a, b, sep), do: a <> sep <> b
end

Concat.join("Hello", "world")        #=> "Hello world"
Concat.join("Hello", "world", "_")   #=> "Hello_world"
```

## Rules
- `def/2` defines a function other modules can call; `defp/2` defines a private function that can only be invoked locally.
- Functions are identified by name and arity (number of arguments); document and refer to them as `Concat.join/3`.
- Function definitions support multiple clauses and guards; Elixir tries each clause until one matches, and an argument matching no clause raises an error (`FunctionClauseError`).
- Use `do:` for one-liners and `do`-blocks for functions spanning multiple lines.
- Default arguments (`\\`) can be any expression; it is evaluated on each call that uses the default, not at definition time.
- If a function with defaults has multiple clauses, declare the defaults in a function head (a definition without a body). Function heads cannot have patterns or guards, only argument names and defaults.

## Self-check
`def join(a, b, sep \\ " ")` makes `join/2` and `join/3` available.

## Checked
Date: 2026-11-02. Confirmed against the Elixir modules-and-functions and anonymous-functions guides (def/defp, name/arity, clauses, do: vs do-block, defaults evaluated per call, function heads for defaults without patterns or guards). Removed: clause grouping warning, overlapping-defaults conflict, predicate naming note, compiler warning text.
Method: documentation only; no commands were run.
