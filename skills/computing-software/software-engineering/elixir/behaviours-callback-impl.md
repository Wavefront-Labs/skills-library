---
id: computing-software.software-engineering.elixir.behaviours-callback-impl
name: behaviours-callback-impl
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, behaviour, callback, impl, optional-callbacks, macrocallback, behaviours-callbacks]
level: practitioner
status: docs-checked
description: "Declare contracts with @callback, implement them with @behaviour and @impl, and swap implementations via config for tests."
sources: ["https://hexdocs.pm/elixir/typespecs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Behaviours and callbacks

**Goal:** define an interface that many modules implement and the caller can swap.

```elixir
defmodule Parser do
  @callback parse(String.t()) :: {:ok, term()} | {:error, term()}
  @callback extensions() :: [String.t()]
  @optional_callbacks extensions: 0
end

defmodule JSONParser do
  @behaviour Parser
  @impl Parser
  def parse(str), do: {:ok, str}
end

def parse(mod, input), do: mod.parse(input)       # dynamic dispatch by module atom
```

## Rules
- `@impl Parser` makes the compiler check that the function is a real callback of that behaviour (a typo such as `parse/0` instead of `parse/1` produces a warning).
- Behaviours dispatch by module; protocols dispatch by data type: choose accordingly.
- Define behaviours for external dependencies you want to mock (see the Mox skill).
- A module that does not implement a required callback gets a compile-time warning. Callbacks listed in `@optional_callbacks` (name: arity) may be left out.

## Failure modes
- Passing a module that lacks the function: dynamic dispatch has no check beyond the compile-time warning.

## Self-check
Remove `parse/1` from `JSONParser` and compile: expect a compile-time warning that a required callback is not implemented.

## Checked

- Date: 2026-11-02.
- Confirmed against the Elixir typespecs reference (hexdocs.pm/elixir/typespecs.html), Behaviours section: `@callback`, `@behaviour`, `@impl`, `@optional_callbacks`, compile-time warning for missing callbacks, warning for mismatched `@impl`, dispatching on a module passed as an argument.
- Removed: `Jason.decode` (library call not on the page), the claim that `@impl true` on one callback requires it on all, and `UndefinedFunctionError`.

Method: documentation only; no commands were run.
