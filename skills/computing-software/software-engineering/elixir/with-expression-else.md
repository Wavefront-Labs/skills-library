---
id: computing-software.software-engineering.elixir.with-expression-else
name: with-expression-else
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, with, else, happy-path, railway, ok-error-chain, with-expression]
level: practitioner
status: docs-checked
description: "Chain fallible steps with with, understand how else handles non-matching values, and avoid hiding error origins with a catch-all else."
sources: ["https://hexdocs.pm/elixir/Kernel.SpecialForms.html#with/1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The with special form

**Goal:** flatten nested `case` matches into one readable chain, following the `Kernel.SpecialForms.with/1` docs.

```elixir
def area(opts) do
  with {:ok, width} <- Map.fetch(opts, :width),
       {:ok, height} <- Map.fetch(opts, :height) do
    {:ok, width * height}
  end
end

with {:ok, content} <- File.read(path),
     :ok <- File.write(path, [content, "!"]) do
  :ok
else
  {:error, reason} ->
    Logger.error("could not append ! to #{path} with reason: #{reason}")
    :error
end

with {:ok, width} <- Map.fetch(opts, :width),
     double_width = width * 2,            # plain `=` clause
     {:ok, height} <- Map.fetch(opts, :height) do
  {:ok, double_width * height}
end
```

## Rules
- `PATTERN <- EXPRESSION` is a sibling of `=`: where `=` raises on no match, `<-` aborts the `with` chain and returns the non-matched value (when there is no `else`).
- If all clauses match, the `do` block runs and its value is returned.
- Expressions without `<-` can appear in clauses; they behave as outside `with`, so a failing `=` raises `MatchError`.
- Variables bound inside `with` are not accessible outside it, nor in the `else` block.
- `else` works like `case`: several clauses, first match wins. If no `else` clause matches, a `WithClauseError` is raised.
- Drawback: all failures are flattened into one `else`, forcing you to rebuild the result types of each step. Prefer to refactor each `<-` step to return the desired error format (for example `validate_extension/1` returning `:ok` or `{:error, reason}`) and keep `else` small or absent.
- Parentheses around the clauses are a matter of preference.

## Self-check
`with {:ok, x} <- {:error, 1}, do: x` returns `{:error, 1}`.

## Checked
Date: 2026-11-02. Confirmed against Kernel.SpecialForms.with/1 docs (<- aborts and returns the non-match, = clauses, scope, else works like case, WithClauseError, flattened-else drawback and refactor). Removed: bare `else error -> error` rule, guards-in-clauses claim, step-count advice.
Method: documentation only; no commands were run.
