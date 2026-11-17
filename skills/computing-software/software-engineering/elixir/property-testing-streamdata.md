---
id: computing-software.software-engineering.elixir.property-testing-streamdata
name: property-testing-streamdata
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, stream-data, property-testing, check-all, generators, shrinking, exunitproperties]
level: advanced
status: draft
description: "Write properties with StreamData generators and check_all so ExUnit explores many inputs and shrinks failures to minimal cases."
sources: ["https://hexdocs.pm/stream_data"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Property-based testing with StreamData

**Goal:** test invariants over generated data.

```elixir
use ExUnit.Case
use ExUnitProperties

property "reverse twice is identity" do
  check all list <- list_of(integer()) do
    assert Enum.reverse(Enum.reverse(list)) == list
  end
end

property "sorted output is ordered" do
  check all xs <- list_of(integer(), min_length: 1), max_runs: 200 do
    sorted = Enum.sort(xs)
    assert sorted == Enum.sort(sorted)
    assert length(sorted) == length(xs)
  end
end
# generators: integer(), string(:alphanumeric), member_of([...]), one_of([...]), map_of(...), tuple({...}),
# constant(x), bind/map/filter (prefer constructive generation over filter)
```

## Rules
- Pick properties: round trips (encode/decode), idempotence, invariants (length, ordering), comparison with a simple model.
- Shrinking reduces a failing input; the seed printed on failure reproduces it (`mix test --seed N`).
- `filter` that rejects most values causes `TooManyConsecutiveFiltersError`-style failures; generate valid data directly.
- Keep properties fast; run fewer runs in CI if needed.

## Self-check
Write a deliberately wrong property and watch it shrink to a small counterexample.
