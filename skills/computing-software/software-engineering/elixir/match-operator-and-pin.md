---
id: computing-software.software-engineering.elixir.match-operator-and-pin
name: match-operator-and-pin
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, pattern-match, pin-operator, destructuring, underscore, match-error, match-operator-pin, elixir-pattern-matching]
level: practitioner
status: docs-checked
description: "= is a match not an assignment; use ^ to match an existing value, _ to ignore, and know the MatchError and rebinding rules."
sources: ["https://hexdocs.pm/elixir/pattern-matching.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The match operator, pin and underscores

**Goal:** destructure data safely and predict when a match fails.

```elixir
{:ok, result} = {:ok, 13}                # binds result
{:ok, result} = {:error, :oops}          # ** (MatchError)
[head | _] = [1, 2, 3]                   # _ ignores the tail
[head | tail] = []                       # ** (MatchError): cannot match an empty list
%{:a => a} = %{:a => 1, 2 => :b}         # map patterns match a subset of the map
{x, x} = {1, 2}                          # ** (MatchError): repeated variable must bind to the same value
x = 1
^x = 2                                   # ** (MatchError): pin matches the existing value
[^x, 2, 3] = [1, 2, 3]                   # pin inside other patterns
{y, ^x} = {2, 1}
```

## Rules
- `=` is the match operator: a variable can only be assigned on the left side, and a failed match raises `MatchError`.
- Variables can be rebound (`x = 1` then `x = 2`); the pin operator `^` matches against the variable's existing value instead of rebinding.
- A map in a pattern matches when the pattern's keys exist in the map, so `%{}` matches every map. Lists and tuples must match in size.
- `_` can never be read from; it is a compile error to use it in an expression.
- You cannot call functions on the left side of a match (`length([1, [2], 3]) = 3` is a compile error).
- Binaries and strings can be matched too, but matching works on bytes unless you use the `utf8` modifier.
- In `case` with no matching clause, `CaseClauseError` is raised; a function called with arguments no clause matches raises `FunctionClauseError`.

## Self-check
`{x, x} = {1, 2}` raises `MatchError`, because a variable mentioned twice in a pattern must bind to one value.

## Checked
Date: 2026-11-02. Confirmed against the Elixir pattern-matching, keywords-and-maps, binaries and modules-and-functions guides (match operator, tuples, lists, head/tail, underscore, repeated variable, pin, map subset, MatchError, FunctionClauseError, CaseClauseError). Removed: string-key map example, prefix-<> example, _name unused-variable warning claim, pinned map key pattern, pin timing claim.
Method: documentation only; no commands were run.
