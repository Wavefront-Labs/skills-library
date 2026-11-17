---
id: computing-software.software-engineering.elixir.typespec-type-spec-opaque
name: typespec-type-spec-opaque
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, typespec, spec, type, typep, opaque, callback, t-type, spec-type, elixir-typespecs]
level: practitioner
status: docs-checked
description: "Declare custom types and function specs with @type/@spec/@typep/@opaque; modules commonly name their main type t()."
sources: ["https://hexdocs.pm/elixir/typespecs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @type, @spec and @typep

**Goal:** annotate public functions so tools and readers know the contract.

```elixir
defmodule Account do
  @type id :: pos_integer()
  @type t :: %__MODULE__{id: id(), balance: integer()}
  @typep internal :: {atom(), term()}      # private to the module
  @opaque token :: binary()                 # callers must not look inside
  defstruct [:id, balance: 0]

  @spec deposit(t(), pos_integer()) :: {:ok, t()} | {:error, :invalid_amount}
  def deposit(%__MODULE__{} = a, n) when n > 0, do: {:ok, %{a | balance: a.balance + n}}
  def deposit(_, _), do: {:error, :invalid_amount}
end
```

## Rules
- Common built-ins: `integer()`, `non_neg_integer()`, `pos_integer()`, `float()`, `atom()`, `binary()`, `String.t()`, `list(t)` / `[t]`, `keyword()`, `map()`, `%{key: value_type}`, `{a, b}`, `term()`, `any()`, `no_return()`, `pid()`, `module()`, `mfa()`, `fun()`, `(a -> b)`.
- Modules commonly define their principal type as `t/0` (for example `Range.t/0`, `String.t/0`). `@typep` is private; `@opaque` keeps the type public but hides its internal structure.
- Typespecs are used by documentation and by tools such as Dialyzer. The docs say they are a notation distinct from Elixir's set-theoretic types and may be phased out as that effort moves forward.
- Specifications can be overloaded, like ordinary functions, with multiple `@spec` lines.
- Type variables use a guard: `@spec function(arg) :: [arg] when arg: var`.

## Self-check
Write `@spec` for `Enum.map`-like `my_map(list(a), (a -> b)) :: list(b)` using the `when a: var, b: var` guard.

## Checked
2026-11-03: confirmed against the Elixir typespecs reference (built-in types, `list(type)`, `[type]`, map forms, `(type1, type2 -> type)`, `@typep`/`@opaque`, overloaded specs, `when arg: var`, `t/0` naming in `Range.t/0`, Dialyzer use, set-theoretic note). Fixed: removed two `@spec` lines without a matching function (the compiler rejects a spec for an undefined function). Removed: the runtime-enforcement remark and the Dialyzer warning claim.
Method: documentation only; no commands were run.
