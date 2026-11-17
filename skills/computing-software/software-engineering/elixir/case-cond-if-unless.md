---
id: computing-software.software-engineering.elixir.case-cond-if-unless
name: case-cond-if-unless
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, case, cond, if, unless, truthy, falsy, case-cond-if, elixir-control-flow]
level: intro
status: docs-checked
description: "Choose case for matching values, cond for several boolean conditions, if for a single condition; only nil and false are falsy."
sources: ["https://hexdocs.pm/elixir/case-cond-and-if.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case, cond, if and unless

**Goal:** pick the right branching construct and avoid nested `if`.

```elixir
case File.read(path) do
  {:ok, body} -> body
  {:error, :enoent} -> ""
  {:error, reason} -> raise "read failed: #{inspect(reason)}"
end

cond do
  x < 0 -> :neg
  x == 0 -> :zero
  true -> :pos          # `true` is the catch-all
end

if x > 0 do :ok else :denied end
```

## Rules
- `case` clauses are tried top to bottom; no match raises `CaseClauseError`. Guards (`when`) add conditions; errors in a guard make it fail rather than raise.
- Only `nil` and `false` are falsy in `if` and `cond`.
- `cond` needs a final `true ->` or it raises `CondClauseError`.
- Variables bound or changed inside `if`/`case` do not leak out; return the value instead of assigning inside the branch.
- Elixir developers generally prefer pattern matching and guards (`case`, multi-clause functions); use `if` when the logic cannot be expressed in patterns and guards, and `cond` when several conditions are needed.

## Self-check
`if false do ... end` with no `else` returns `nil`.

## Checked

- Date: 2026-11-02.
- Confirmed against the Elixir guide page "case, cond, and if" (hexdocs.pm/elixir/case-cond-and-if.html): clause order, `CaseClauseError`, `CondClauseError` and the final `true ->`, falsy only for `nil`/`false`, `if` without `else` returning `nil`, scoping of variables, and the preference for pattern matching with `case` and function clauses.
- Removed: the claim about `unless` style guidance (not stated on the page).

Method: documentation only; no commands were run.
