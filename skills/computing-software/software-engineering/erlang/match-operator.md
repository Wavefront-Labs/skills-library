---
id: computing-software.software-engineering.erlang.match-operator
name: match-operator
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-pattern, match-operator]
level: intro
status: docs-checked
description: "Erlang `=` as pattern match: destructuring tuples, lists, maps, repeated variables, the = pattern alias and badmatch."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pattern matching and the match operator
**Goal:** destructure data in function heads and expressions.

```erlang
{ok, [First | Rest]} = {ok, [1,2,3]},
#{name := Name} = #{name => <<"ann">>, age => 3},
[_|_] = L = [1,2],               % compound pattern: bind whole and match shape
```
- A failed `Pattern = Expr` raises `{badmatch, Value}`; no matching function clause raises `function_clause`; no matching case branch raises `{case_clause, V}`.
- Chained matches are evaluated right to left: `{A, B} = T = {answer, 42}` binds `T` first.
- Map patterns use `:=` only and match a subset of keys; `#{}` matches any map (a non-map raises `badmatch`).
- String prefix pattern: `"abc" ++ Rest` is sugar for matching the list of characters; for binaries use `<<"abc", Rest/binary>>`.
- A compound pattern `Pattern1 = Pattern2` matches both against the same term (useful in heads: `f({connect,_,To,_,_} = Signal, To)`). Operands are not matched in any defined order, so a variable bound in one cannot be used in the other.
- Arithmetic is allowed in patterns only with numeric or bitwise operators that evaluate to a constant at compile time.

## Gotchas
- `++` in a pattern works only for a literal string prefix.

## Self-check
Destructure a nested tuple, a map and a list prefix, then force a badmatch.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Patterns, Compound Pattern Operator, String Prefix, Expressions in Patterns, Match Operator, Maps in Patterns), "Errors and Error Handling" (badmatch, function_clause, case_clause). Removed: the `{A, A} = {1, 1}` and `X = 1, X = 1` examples (variable rebinding rules were not re-read for this batch).
Method: documentation only; no commands were run.
