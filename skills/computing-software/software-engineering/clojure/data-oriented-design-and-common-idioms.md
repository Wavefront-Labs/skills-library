---
id: computing-software.software-engineering.clojure.data-oriented-design-and-common-idioms
name: data-oriented-design-and-common-idioms
category: computing-software
field: software-engineering
product: clojure
tags: [clojure, idioms, data-oriented, maps-over-objects, pure-functions, immutability, rich-comment, simple-made-easy, naming, idioms-data-oriented]
level: practitioner
status: draft
description: "Write data-oriented Clojure: prefer plain maps and functions over classes, keep functions pure, use qualified keys, and structure code around transformations of data."
sources: ["https://clojure.org/guides/learn/functions", "https://github.com/bbatsov/clojure-style-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data-oriented idioms

**Goal:** the shape of idiomatic, maintainable Clojure.

- Model entities as maps with namespaced keys (`:user/id`, `:user/email`); add schemas at boundaries.
- Write small pure functions `data -> data`; compose with `->`, `reduce`, `into` and transducers.
- Keep side effects at the edges; return descriptions of effects as data when helpful (effects-as-data, e.g. a
  vector of commands interpreted by a runner).
- Use `update`, `assoc-in`, `merge` rather than building classes; use `select-keys` to project.
- Prefer `if-let`, `when-let`, `some->` for optional values; use `nil` punning (`(seq xs)`, `(empty? xs)`).
- Choose collection functions by the result you need: `map` (lazy), `mapv` (vector), `into` (any), `reduce` (fold).
- Use protocols for polymorphism on type, multimethods for dispatch on data, `case` for closed sets.
- Name things for what they are: avoid `data`, `result`, `info`; use `->` chains with intent-revealing helpers.
- Put exploratory code in `(comment ...)` blocks; delete dead code.
- Test with example data and property tests, not mocks; build "sample" data fixtures as plain maps.
- Be wary of abstractions you do not need yet; copy a little before generalising.

## Failure modes
- Deeply nested anonymous functions (extract named functions).
- Mixing keyword and string keys in the same map after JSON round trips (normalise at the boundary).

## Self-check
Pick a function in your codebase that mutates or hides state and rewrite it as a pure data transformation.
