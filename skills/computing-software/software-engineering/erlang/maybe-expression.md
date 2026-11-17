---
id: computing-software.software-engineering.erlang.maybe-expression
name: maybe-expression
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-expressions, maybe-expression]
level: advanced
status: docs-checked
description: "Erlang maybe ... end for short-circuit error flow: feature flag in OTP 25 and 26, on by default from OTP 27."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# maybe expression with ?=
**Goal:** chain fallible steps without nested case.

```erlang
-feature(maybe_expr, enable).   % needed on OTP 25 and 26; enabled by default from OTP 27
read_port(Cfg) ->
    maybe
        {ok, Raw} ?= maps:find(port, Cfg),
        {Port, <<>>} ?= string:to_integer(Raw),
        {ok, Port}
    else
        error -> {error, no_port};
        {error, no_integer} -> {error, bad_port}
    end.
```
- `Pattern ?= Expr` is only allowed at the top level of a `maybe` block. If it matches the block continues; if not, the rest of the block is skipped and the block returns the value of `Expr` (or the `else` clauses are tried).
- With `else`, the unmatched value must match an else clause, or an `else_clause` run-time error occurs.
- A plain `=` match that fails inside the block raises `badmatch` as usual.
- Variables bound in a `maybe` block must not be used after it or in the `else` clauses.
- Other ways to enable the feature: `erlc -enable-feature maybe_expr`, or the compiler option `{feature, maybe_expr, enable}`. The `-feature` directive is the preferred method.

## Gotchas
- Without an `else`, the non-matching value is returned as is, which can leak internal shapes.

## Self-check
Compile on your OTP and test both the success and failure return paths.

## Checked
2026-11-02. Erlang Reference Manual "Expressions" (Maybe section: `?=`, else, `else_clause`, variable scope, OTP 25 introduction and OTP 27 default), "Features" (enabling methods, `maybe_expr` approved in OTP 27, directive preferred). `string:to_integer/1` return shapes from the STDLIB string module docs. Removed: the unconfirmed `{enable_feature, maybe_expr}` option.
Method: documentation only; no commands were run.
