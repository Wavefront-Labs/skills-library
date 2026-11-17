---
id: computing-software.software-engineering.elixir.nested-get-in-put-in-update-in
name: nested-get-in-put-in-update-in
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, get-in, put-in, update-in, access-behaviour, pop-in, access-key, access-all, nested-access]
level: practitioner
status: docs-checked
description: "Read and update nested maps/lists/keyword lists with the Access-based get_in/put_in/update_in and the macro path form."
sources: ["https://hexdocs.pm/elixir/Access.html", "https://hexdocs.pm/elixir/Kernel.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested access: get_in, put_in, update_in

**Goal:** read and change deep structures with `Access` and the `Kernel` nested-access functions.

```elixir
users = %{"john" => %{age: 27}, "meg" => %{age: 23}}
get_in(users["john"].age)                     #=> 27
get_in(users["unknown"].age)                  #=> nil (no raise, unlike plain access on nil)
put_in(users["john"].age, 28)                 # macro (path) form
update_in(users, ["john", :age], &(&1 + 1))   # function (keys) form

languages = [%{name: "elixir", type: :functional}, %{name: "c", type: :procedural}]
user = %{name: "john", languages: languages}
get_in(user, [:languages, Access.all(), :name])                      #=> ["elixir", "c"]
update_in(user, [:languages, Access.all(), :name], &String.upcase/1)
get_in(languages, [Access.at(1), :name])                             #=> "c"
pop_in(salaries, [Access.filter(&(&1.salary >= 20)), :name])

get_and_update_in(map.user.name, fn prev -> {prev, String.upcase(prev)} end)
get_in(map, [Access.key(:user), Access.key(:name)])    # Access.key/2 for map, struct or keyword
```

## Rules
- `map[key]` is loose (returns `nil` for a missing key); `map.key` is strict (raises for a missing key or a `nil` map). Prefer `map.key` for predefined atom keys. `get_in/1` bridges the gap by returning `nil` through `nil` values.
- The `Access` syntax works with maps and keyword lists (and structs that implement the `Access` behaviour). Plain structs do not allow `struct[key]`; use the `struct.key` syntax, such as `put_in(struct.foo.bar, :baz)` (the complete path must be visible to the macro), or `Access.key/2` / `Access.key!/1` in a key path.
- Accessor functions: `Access.all/0` (every list element), `Access.at/1` (index, negative from the end), `Access.filter/1` (elements matching a function; an empty list is returned when nothing matches), `Access.key/2` (with a default), `Access.key!/1` (raises `KeyError` when missing), `Access.elem/1`.
- `update_in/3` passes the current value (`nil` if absent) to the function; if an intermediate value is `nil` it raises `ArgumentError` ("could not put/update key ... on a nil value").
- Dot notation cannot remove fields, as those fields must be present.

## Self-check
Convert every language name in a user map to uppercase with `update_in/3` and `Access.all/0`.

## Checked
Date: 2026-11-02. Confirmed against the Access module docs and Kernel get_in, put_in, update_in docs (map[key] vs map.key, nested paths, Access.all/at/filter/key/key!, struct caveat, nil handling, dot notation limits). Removed: pop_in/get_and_update_in struct claim details, UndefinedFunctionError failure-mode text, restructuring advice.
Method: documentation only; no commands were run.
