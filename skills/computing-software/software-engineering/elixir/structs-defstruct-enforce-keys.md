---
id: computing-software.software-engineering.elixir.structs-defstruct-enforce-keys
name: structs-defstruct-enforce-keys
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, struct, defstruct, enforce-keys, update-syntax, derive, structs]
level: practitioner
status: docs-checked
description: "Define structs with defstruct and @enforce_keys, use the %{s | k: v} update that only touches existing keys, and understand they are maps with __struct__."
sources: ["https://hexdocs.pm/elixir/structs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Structs

**Goal:** model fixed-shape domain data.

```elixir
defmodule Car do
  @enforce_keys [:make]
  defstruct [:model, :make]
end

defmodule User do
  defstruct [:email, name: "John", age: 27]   # keyword defaults must come last
end

john = %User{}
john.name                         #=> "John"
jane = %{john | name: "Jane"}     # update syntax; raises KeyError for a key not in the struct
%User{name: name} = john          # match on the struct type and keys
struct!(john, name: "Jane", age: 30)   # dynamic update from a keyword list or map
struct(User, name: "meg")         # runtime build; unknown keys are ignored
```

## Rules
- A struct is a map with a special `__struct__` field holding the module name (`is_map(john)` is true).
- Structs share the field access and update syntax of fixed-key maps, but do not inherit map features: `john[:name]` fails because `Access` is not implemented, and `Enum.each/2` fails because `Enumerable` is not implemented. Protocols can attach such behaviour to a struct.
- `@enforce_keys` raises `ArgumentError` ("the following keys must also be given when building struct Car: [:make]") when a key is missing at build time. It is not enforced on updates and does not validate values.
- `struct!/2` checks key validity like the literal syntax (and enforces `@enforce_keys` when building); `struct/2` silently ignores unknown keys and string keys. The guide recommends `struct!/2` over `Map` functions for dynamic updates.
- Use the update syntax (`%{john | name: "Jane"}`) when you know the fields at compile time.
- `%User{} = %{}` raises `MatchError`: matching `%User{}` also checks that the value is a User struct.
- Protocol implementations can be derived with `@derive` when the protocol implements `Any` (see the protocols guide).

## Self-check
`%Car{}` raises `ArgumentError` because `:make` is enforced.

## Checked
Date: 2026-11-02. Confirmed against the Elixir structs guide, Kernel.struct/2 and struct!/2 docs (__struct__ field, access/update syntax, no Access or Enumerable, @enforce_keys error and limits, defaults order, struct vs struct!, pattern matching). Removed: @type example, is_struct and Map.from_struct usage, Jason.Encoder derive example, compile-time error self-check.
Method: documentation only; no commands were run.
