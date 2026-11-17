---
id: computing-software.software-engineering.elixir.guards-multi-clause-matching
name: guards-multi-clause-matching
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, guard, defguard, when, is-integer, function-clause-error, guards-clauses]
level: practitioner
status: docs-checked
description: "Write guards with the allowed Kernel functions, understand why a failing guard just skips the clause, and define reusable defguard macros."
sources: ["https://hexdocs.pm/elixir/patterns-and-guards.html", "https://hexdocs.pm/elixir/Kernel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guards and multi-clause matching

**Goal:** restrict clauses with guards that compile and behave as expected, following the Elixir patterns-and-guards reference.

```elixir
def empty_map?(map) when map_size(map) == 0, do: true
def empty_map?(map) when is_map(map), do: false

defmodule MyInteger do
  defguard is_even(term) when is_integer(term) and rem(term, 2) == 0
end

import MyInteger, only: [is_even: 1]
def my_function(number) when is_even(number), do: :even

# multiple guards: the clause runs if any guard passes
def empty?(val)
    when map_size(val) == 0
    when tuple_size(val) == 0,
    do: true
def empty?(_val), do: false

match?({:ok, value} when value > 0, {:ok, 13})
```

## Rules
- Guards start with `when`; a clause runs if and only if its guard evaluates to `true`. Any other value (even a truthy one like `"some_value"`) skips the clause: write `when head != nil`, not `when head`.
- Only a handful of expressions are allowed, deliberately, so guards are predictable and efficient: comparison operators, `max`/`min`, strictly boolean `and`/`or`/`not` (`&&`, `||` and `!` are NOT allowed), arithmetic operators, `in`/`not in` with a list or range on the right, type checks like `is_list/1`, functions on built-in types (`abs/1`, `hd/1`, `map_size/1`), and `map.field`. See `Kernel` for the full list. Macros built from these (for example `Integer.is_even/1`) are valid guards.
- If a function in a guard would raise, the guard fails instead and the next clause is tried. In an `or` chain this can hide a result (`map_size/1` on a tuple fails the whole guard); use type checks first, or multiple `when` guards, which are tried in turn.
- `defguard/1` and `defguardp/1` define custom guards and perform additional compile-time checks; prefer them to hand-written macros.
- Guards work in function clauses, `case`, `match?/2` and other pattern-matching constructs.
- If no clause matches, `FunctionClauseError` is raised.

## Self-check
Predict `empty?({})` for the single `or` guard version (`false`) versus the multiple-guard version (`true`).

## Checked
Date: 2026-11-02. Confirmed against the Elixir patterns-and-guards reference (allowed expressions, && || ! not allowed, true-only rule, errors fail the guard, multiple guards, defguard, where guards are allowed). Removed: n in 1..10 case example, FunctionClauseError listing claim, clause-order warning, hd/length/elem/byte_size/is_map_key enumeration (see Kernel).
Method: documentation only; no commands were run.
