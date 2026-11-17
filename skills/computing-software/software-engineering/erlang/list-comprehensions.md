---
id: computing-software.software-engineering.erlang.list-comprehensions
name: list-comprehensions
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-expressions, list-comprehensions]
level: practitioner
status: docs-checked
description: "Erlang comprehensions: generators, filters, patterns that skip non-matches, map comprehensions from OTP 26."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# List and map comprehensions
**Goal:** transform collections concisely.

```erlang
[X * X || X <- lists:seq(1, 5), X rem 2 =:= 1].       % [1,9,25]
[V || {ok, V} <- [{ok,1},{error,x},{ok,3}]].          % [1,3] (non-match skipped)
[{X,Y} || X <- [1,2], Y <- [a,b]].                    % nested generators
#{K => V * 2 || K := V <- #{a => 1, b => 2}}.         % map comprehension, OTP 26+
```
- A filter is an expression that evaluates to `true` or `false`. If the filter is a guard expression, a failure or non-boolean value counts as `false`; otherwise a non-boolean value raises `{bad_filter, Val}`.
- Variables bound in a generator are not visible outside the comprehension; generator variables shadow earlier bindings.
- Strict generators (`<:-`) and zip generators were introduced in OTP 28; strict is the better practice when either works.
- The same qualifiers build binaries (`<< ... || ... >>`).

## Gotchas
- Using a comprehension for side effects builds a throwaway list; use `lists:foreach/2`.

## Self-check
Run the pattern-skipping example and compare with `lists:filtermap/2`.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Comprehensions: syntax, OTP 26 map comprehensions, OTP 28 strict and zip generators, filter semantics and `bad_filter`, variable scope). Removed: the unconfirmed OTP 28 hedge (now confirmed) and the earlier wrong `bad_filter` statement for guard-expression filters.
Method: documentation only; no commands were run.
