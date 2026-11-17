---
id: computing-software.software-engineering.erlang.abstract-format
name: abstract-format
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-compiler, abstract-format]
level: sme
status: draft
description: "Erlang abstract format tooling: erl_scan, erl_parse, epp, erl_pp, erl_eval and beam_lib chunks."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Abstract code, scanning and parsing
**Goal:** read and generate Erlang source programmatically.

```erlang
{ok, Tokens, _} = erl_scan:string("foo(X) -> X + 1."),
{ok, Form} = erl_parse:parse_form(Tokens),
Src = erl_pp:form(Form),
{ok, Forms} = epp:parse_file("src/mymod.erl", []),
{ok, Exprs} = erl_parse:parse_exprs(element(2, erl_scan:string("1 + 2."))),
{value, 3, _} = erl_eval:exprs(Exprs, erl_eval:new_bindings()).
```
- `beam_lib:chunks(Beam, [abstract_code])` returns abstract code only if compiled with `debug_info` (newer releases store it in a `debug_info` chunk; check docs).
- `erl_eval` interprets expressions and is what the shell uses; it is slower than compiled code and allows arbitrary execution, so never feed it untrusted text.

## Gotchas
- Modifying abstract code without recompiling does nothing; you must `compile:forms/2`.

## Self-check
Scan, parse and pretty-print a function, then compile it with `compile:forms/2`.
