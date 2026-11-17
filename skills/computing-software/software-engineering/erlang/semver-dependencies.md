---
id: computing-software.software-engineering.erlang.semver-dependencies
name: semver-dependencies
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-hex, semver-dependencies]
level: practitioner
status: draft
description: "Erlang library versioning on Hex: semver, ~> constraints, compatibility and lock files."
sources:
  - https://rebar3.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Semantic versioning and constraints
**Goal:** depend on and release versions safely.

- Hex uses Semantic Versioning: breaking changes bump MAJOR, additive changes MINOR, fixes PATCH.
- Constraint `"~> 2.10"` allows `>= 2.10.0 and < 3.0.0`; `"~> 2.10.1"` allows `>= 2.10.1 and < 2.11.0`.
- Libraries should use ranges so consumers can resolve; releases (applications) pin via `rebar.lock`.
- Maintain a changelog; deprecate before removing: `-deprecated([{old_fun, 1, "use new_fun/1"}]).` (xref `deprecated_function_calls` flags callers).
- Keep `.app.src` `vsn` equal to the tag you publish.

## Gotchas
- Wide ranges on transitive dependencies cause conflicts; resolve by overriding in the top app.

## Self-check
Add a `~>` dep and verify which version is locked.
