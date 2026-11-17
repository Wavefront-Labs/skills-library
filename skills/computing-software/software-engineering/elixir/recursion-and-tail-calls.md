---
id: computing-software.software-engineering.elixir.recursion-and-tail-calls
name: recursion-and-tail-calls
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, recursion, tail-call-optimization, accumulator, reduce, recursion-tail]
level: practitioner
status: docs-checked
description: "Write recursive functions with accumulators so the call is in tail position; prefer Enum for list work."
sources: ["https://hexdocs.pm/elixir/recursion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Recursion and tail calls

**Goal:** loop without mutable state, following the Elixir recursion guide.

```elixir
defmodule Math do
  # reduce algorithm: accumulator, the recursive call is the last expression
  def sum_list([head | tail], accumulator), do: sum_list(tail, head + accumulator)
  def sum_list([], accumulator), do: accumulator

  # map algorithm: build a new list
  def double_each([head | tail]), do: [head * 2 | double_each(tail)]
  def double_each([]), do: []
end

# usually better: Enum
Enum.reduce([1, 2, 3], 0, &+/2)     #=> 6
Enum.map([1, 2, 3], &(&1 * 2))      #=> [2, 4, 6]
```

## Rules
- Elixir has no loop constructs; data is immutable, so loops are recursion plus high-level functions for collections.
- A function with several clauses runs the first clause whose patterns and guards match; the clause that stops the recursion (empty list, `0`) is the terminal case.
- Recursion and tail call optimization are an important part of Elixir for creating loops, but you will rarely write recursion by hand to manipulate lists: prefer `Enum` (and `Stream` for lazy work).
- If no clause matches (for example a negative count when the guard is `n > 0`), a `FunctionClauseError` is raised.

## Self-check
Rewrite `sum_list/2` and `double_each/1` with `Enum.reduce/3` and `Enum.map/2`.

## Checked
Date: 2026-11-02. Confirmed against the Elixir recursion guide (no loop constructs, terminal clause, reduce and map algorithms, Enum alternatives, FunctionClauseError, tail call optimisation mentioned). Removed: stack-growth claims, try/rescue non-tail-call rule, speed comparison and Benchee advice, server-loop rules, million-element test.
Method: documentation only; no commands were run.
