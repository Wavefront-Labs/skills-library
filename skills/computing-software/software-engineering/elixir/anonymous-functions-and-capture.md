---
id: computing-software.software-engineering.elixir.anonymous-functions-and-capture
name: anonymous-functions-and-capture
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, fn, capture-operator, closure, arity, function-reference, anonymous-functions, elixir-functions]
level: intro
status: docs-checked
description: "Build fn and & captures, call them with dot syntax, and capture named functions with &Mod.fun/arity."
sources: ["https://hexdocs.pm/elixir/anonymous-functions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anonymous functions and the capture operator

**Goal:** write and pass functions correctly.

```elixir
add = fn a, b -> a + b end
add.(1, 2)                         # the dot is required for anonymous functions
double = &(&1 * 2)                 # capture shorthand
Enum.map(["a"], &String.upcase/1)  # capture a named function
f = &Kernel.+/2                    # operators can be captured
fn
  0 -> :zero
  n when n > 0 -> :pos
end
x = 10; g = fn -> x end; x = 20; g.() #=> 10 (closure keeps the value at creation)
is_function(add, 2)
```

## Rules
- `&1`, `&2` are positional args.
- Use `&Mod.fun/arity` rather than `fn x -> Mod.fun(x) end`.
- A function created with `fn` can have multiple clauses and guards; all clauses must have the same arity.

## Failure modes
- Calling `add(1, 2)` without the dot looks for a named function `add/2`, not the anonymous function.

## Self-check
`(&(&1 <> "!")).("hi")` returns `"hi!"`.

## Checked
2026-11-02: confirmed against Elixir getting-started "Anonymous functions" (dot call, arity, is_function/2, closures). Removed: capture nesting rule, BadArityError and compile-message wording.
Method: documentation only; no commands were run.
