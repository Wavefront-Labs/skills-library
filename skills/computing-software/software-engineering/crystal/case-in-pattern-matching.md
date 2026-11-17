---
id: computing-software.software-engineering.crystal.case-in-pattern-matching
name: case-in-pattern-matching
category: computing-software
field: software-engineering
product: crystal
tags: [case-in-pattern-matching, case-when, case-in, exhaustive, pattern-matching, enum-match, union-match, crystal]
level: practitioner
status: docs-checked
description: "Use exhaustive case/in in Crystal over unions, Bool, enums and tuple literals."
sources:
  - https://github.com/crystal-lang/crystal-book/blob/master/docs/syntax_and_semantics/case.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# case/in exhaustive matching

Goal: get compiler-checked exhaustiveness.

- `in` instead of `when` makes the case exhaustive: omitting a required condition is a compile-time error, and the case cannot contain `when` or `else`.
- Union: each member type, and `in nil` (or `Nil`; `.nil?` is not allowed).
- `Bool`: `in true` / `in false`.
- Non-flags enum: members as constants (`in Foo::X`) or predicates (`in .y?`); `in .z?` is allowed but `:z` is not.
- Tuple literal subject: conditions must cover all combinations, e.g. `in {true, _}` and `in {_, false}`; the error lists the missing cases (`{false, true}`).
- Adding an enum member then breaks the build until handled.

Verify: add a new enum member and watch the build fail until handled.

## Checked
Checked 2026-11-02 against the crystal-book `case` page. Removed: array, NamedTuple and `.method?` patterns, guards, version remarks, the claim that mixing is "not allowed" beyond the documented no-`when`/`else` rule.

Method: documentation only; no commands were run.
