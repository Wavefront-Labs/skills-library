---
id: computing-software.software-engineering.elixir.protocols-defprotocol-defimpl
name: protocols-defprotocol-defimpl
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, protocol, defprotocol, defimpl, for-any, fallback-to-any, consolidation, protocols-defimpl, elixir-protocols-behaviours]
level: practitioner
status: docs-checked
description: "Define polymorphism over data types with defprotocol/defimpl, derive implementations and understand protocol consolidation."
sources: ["https://hexdocs.pm/elixir/protocols.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Protocols and implementations

**Goal:** dispatch behaviour on the type of the first argument, following the Elixir protocols guide.

```elixir
defprotocol Size do
  @doc "Calculates the size (and not the length!) of a data structure"
  def size(data)
end

defimpl Size, for: BitString do
  def size(string), do: byte_size(string)
end
defimpl Size, for: Map do
  def size(map), do: map_size(map)
end
defimpl Size, for: Tuple do
  def size(tuple), do: tuple_size(tuple)
end

defimpl Size, for: MapSet do        # structs need their own implementation
  def size(set), do: MapSet.size(set)
end

# derive from Any for one struct
defimpl Size, for: Any do
  def size(_), do: 0
end
defmodule OtherUser do
  @derive [Size]
  defstruct [:name, :age]
end
```

## Rules
- A protocol lets code outside the original module add behaviour for new types; dispatch works for any type that implements the protocol, and the implementations can be spread over many files.
- Types you can implement a protocol for: `Atom`, `BitString`, `Float`, `Function`, `Integer`, `List`, `Map`, `PID`, `Port`, `Reference`, `Tuple`, and structs (plus `Any`).
- Structs are maps but do not share protocol implementations with maps: each struct needs its own `defimpl`, or a derived/fallback `Any` implementation.
- Two ways to use `Any`: `@derive [Protocol]` on the struct (explicit), or `@fallback_to_any true` in the protocol (opt-in; every type without an implementation then gets the `Any` behaviour). For most protocols, raising when no implementation exists is the better default.
- Calling a protocol on a type with no implementation raises `Protocol.UndefinedError` ("protocol Size not implemented for ...").
- The data to dispatch on must be the first argument of every protocol function.
- Built-in protocols include `Enumerable` (used by `Enum`), `String.Chars` (`to_string/1`, used by string interpolation) and `Inspect` (used by `inspect/1` and IEx).
- Protocol consolidation is applied by default to all Mix projects during compilation; see the `Protocol` docs for the details when implementations live outside the compiled paths.

## Self-check
Call `Size.size(%{a: 1})`, then `Size.size([1, 2, 3])` and read the `Protocol.UndefinedError`.

## Checked
Date: 2026-11-02. Confirmed against the Elixir protocols guide and Protocol docs (types list, struct implementations, derive and fallback to Any, UndefinedError, first argument, built-in protocols, consolidation default). Removed: Collectable and List.Chars as built-ins, consolidation caveat for scripts, @spec t example, User roles impl, dispatch-order claims.
Method: documentation only; no commands were run.
