---
id: computing-software.software-engineering.elixir.naming-conventions-elixir
name: naming-conventions-elixir
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, naming, snake-case, question-mark, bang, is-prefix, underscore, convention, naming-conventions, elixir-naming-style]
level: intro
status: docs-checked
description: "Follow Elixir naming: snake_case functions, CamelCase modules, ?-suffix predicates, !-suffix raising variants, is_ for guards, and leading underscore for unused values."
sources: ["https://hexdocs.pm/elixir/naming-conventions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming conventions

**Goal:** name things as the Elixir reference expects.

```elixir
some_map = %{this_is_a_key: "and a value"}   # snake_case variables, functions, attributes
OptionParser                                  # aliases/modules: CamelCase
ExUnit.CaptureIO                              # acronyms keep their capitals
{:ok, _contents} = File.read("README.md")     # leading underscore: value not used
File.read/1  and  File.read!/1                # {:ok, _} | {:error, _}  vs value or raise
String.contains?/2                            # boolean, trailing ?
is_list/1                                     # guard-safe check, is_ prefix
```

## Rules
- Casing: `snake_case` for variables, function names and module attributes; aliases (module names) are `CamelCase`. Atoms may be `:snake_case` or `:CamelCase`, the convention is snake case. Filenames usually follow the `snake_case` of the module (`MyApp` in `my_app.ex`), but this is only a convention.
- A leading underscore marks a value you do not use. Functions starting with an underscore are never imported by default; names like `__info__/1` and `__MODULE__/0` carry compile-time metadata.
- `foo!` is the variant that raises on failure, often paired with a `foo` that returns `:ok`/`:error` tuples (`File.read/1`, `File.read!/1`). A bang can exist without a non-bang twin. Errors from invalid argument types raise whether or not the name has a bang.
- `foo?` returns a boolean (`Keyword.keyword?/1`, `String.contains?/2`). Checks usable in guards use the `is_` prefix instead (`is_list/1`, `Integer.is_even/1`); never combine `?` with `is_`.
- `size` in a name means constant time (`map_size/1`); `length` means linear time (`length/1`, `String.length/1`).
- For key-value structures: `get` returns a default (`nil` unless given) for a missing key, `fetch` returns `:error` or `{:ok, value}`, `fetch!` raises (`Map.get/2`, `Map.fetch/2`, `Map.fetch!/2`).
- `compare/2` returns `:lt`, `:eq` or `:gt`.

## Self-check
Rename a predicate `isAdmin` to the conventional form: `admin?` for a normal function, `is_admin` only if it must work in guards.

## Checked
Date: 2026-11-02. Confirmed against references/naming-conventions (casing, underscore, bang, question mark, is_ prefix, size vs length, get/fetch/fetch!, compare). Removed: defguard, to_x/from_x conventions, get_/set_ prefix advice, file extension rule, underscore-private-function advice.
Method: documentation only; no commands were run.
