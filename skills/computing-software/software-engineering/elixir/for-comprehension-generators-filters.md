---
id: computing-software.software-engineering.elixir.for-comprehension-generators-filters
name: for-comprehension-generators-filters
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, for, comprehension, generator, filter, into, reduce, uniq, comprehensions]
level: practitioner
status: docs-checked
description: "Use for with multiple generators, filters, pattern-matching generators, :into, :uniq and :reduce options in place of nested Enum calls."
sources: ["https://hexdocs.pm/elixir/Kernel.SpecialForms.html#for/1"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# for comprehensions

**Goal:** build a data structure from enumerables or bitstrings with generators, filters, `:into`, `:uniq` and `:reduce`, following the `Kernel.SpecialForms.for/1` docs.

```elixir
for n <- [1, 2, 3, 4], do: n * 2                          #=> [2, 4, 6, 8]
for x <- [1, 2], y <- [2, 3], do: x * y                   #=> [2, 3, 4, 6]  (two generators)
for n <- [1, 2, 3, 4, 5, 6], rem(n, 2) == 0, do: n        #=> [2, 4, 6]     (filter)

users = [user: "john", admin: "meg", guest: "barbara"]
for {type, name} when type != :guest <- users do          # pattern + guard in a generator
  String.upcase(name)
end                                                       #=> ["JOHN", "MEG"]

for <<r::8, g::8, b::8 <- pixels>>, do: {r, g, b}         # bitstring generator
for <<c <- " hello world ">>, c != ?\s, into: "", do: <<c>>   #=> "helloworld"
for x <- [1, 1, 2, 3], uniq: true, do: x * 2              #=> [2, 4, 6]

for <<x <- "AbCabCABc">>, x in ?a..?z, reduce: %{} do
  acc -> Map.update(acc, <<x>>, 1, & &1 + 1)
end                                                       #=> %{"a" => 1, "b" => 2, "c" => 1}
```

## Rules
- Generators use `<-` to extract values from an enumerable (or bitstring) and match them against the pattern on the left; values that do not match the pattern are removed.
- Filters must evaluate to truthy values (everything but `nil` and `false`); a falsy filter discards the current value. A variable assignment used as a filter must also return a truthy value, otherwise values are discarded (move it into the `do` block, or wrap the right side in a list as a generator).
- Variables assigned inside a comprehension are not visible outside it.
- `:into` accepts any structure that implements `Collectable` (for example a string, or `IO.stream()`); the result is a list by default.
- `:uniq` only adds results not returned before.
- `:reduce` (since Elixir v1.8) takes the initial accumulator; the `do` block then uses `->` clauses where the left side receives the accumulator and the right side returns the next one. It avoids traversing the data twice compared to a comprehension plus `Enum.reduce/3`.

## Self-check
`for x <- [1, 2], into: "", do: to_string(x)` returns `"12"` (the `Collectable` string accepts binaries).

## Checked
Date: 2026-11-02. Confirmed against Kernel.SpecialForms.for/1 docs (generators, filters truthy, pattern/guard generators, bitstring generators, :into Collectable, :uniq, :reduce since v1.8, variable scope). Removed: eager vs Stream claim, tuple-skip example with error, map :into example.
Method: documentation only; no commands were run.
