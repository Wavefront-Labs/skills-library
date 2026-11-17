---
id: computing-software.software-engineering.elixir.code-anti-patterns-comments-long-params
name: code-anti-patterns-comments-long-params
category: computing-software
field: software-engineering
product: elixir
tags: [elixir, anti-pattern, primitive-obsession, long-parameter-list, complex-else-with, dynamic-atom-creation, non-assertive-map-access, code-anti-patterns, elixir-anti-patterns]
level: practitioner
status: docs-checked
description: "Recognise the official code anti-patterns (comments overuse, long parameter lists, non-assertive access, dynamic atoms, complex else in with) and the official refactors."
sources: ["https://hexdocs.pm/elixir/code-anti-patterns.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code-related anti-patterns

**Goal:** spot and refactor the code smells listed in the Elixir anti-patterns guide.

```elixir
# Non-assertive map access: map.key for required keys, map[:key] for optional ones
{point.x, point.y, point[:z]}

# Dynamic atom creation: do not convert uncontrolled strings to atoms
status = String.to_existing_atom(status, [:ok, :error, :redirect])

# Complex `else` in with: normalise return types in private helper functions

# Long parameter list: group related arguments into a map or struct
```

## Rules
- Documented code smells: comments overuse, complex `else` clauses in `with`, complex extractions in clauses, dynamic atom creation, long parameter list, namespace trespassing, non-assertive map access, non-assertive pattern matching, non-assertive truthiness, structs with 32 fields or more.
- `map.key` raises `KeyError` when the key is missing (use for structs and maps with known atom keys); `map[:key]` returns `nil` (use for optional keys and any `Access` data structure).
- Atoms are not garbage collected; the VM default limit is 1 048 576 atoms. Replace `String.to_unsafe_atom/1` with `String.to_existing_atom/2` and a list of expected atoms, pattern-match strings to atoms, or use `String.to_existing_atom/1` when neither works (it has pitfalls related to code loading).
- Non-assertive pattern matching: write pattern matches so an unexpected input fails (crashes) near the cause instead of returning a defensive value; supervised processes localise the effect of the error.
- Non-assertive truthiness: `&&`, `||` and `!` treat only `nil` and `false` as falsy; prefer `and`, `or`, `not` when operands are expected to be booleans.
- Namespace trespassing: a package named `:my_lib` should define all its modules under `MyLib`.

## Self-check
Find one place where a required key is read with `map[:key]`, or a string is converted to an atom, and rewrite it as above.

## Checked
Date: 2026-11-02. Confirmed against the Elixir anti-patterns page code-anti-patterns (elixir-lang/elixir lib/elixir/pages): smell list, map.key vs map[:key], atom limit and to_existing_atom options, truthiness, namespace trespassing. Removed: speculative assumptions, working with invalid data and complex branching as listed smells, to_atom example, let-it-crash wording, primitive obsession advice (it is a design smell).
Method: documentation only; no commands were run.
