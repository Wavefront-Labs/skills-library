---
id: computing-software.systems-network-administration.icinga-2.dsl-functions-lambdas-scopes-and-control-flow
name: dsl-functions-lambdas-scopes-and-control-flow
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, dsl, functions, lambda, closures, scopes, if-else, for-loop, try-except]
level: practitioner
status: docs-checked
description: "Write Icinga 2 DSL logic: functions, lambdas, use() closures, scopes, if/else, loops, try/except, constructors and types."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/17-language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DSL functions, scopes and control flow
**Functions:** `function multiply(a, b) { return a * b }`. Without `return`, the value of the last expression is returned; bare `return` gives `null`. Anonymous: `var fn = function() { 3 }`.

**Lambdas:** `f = (x) => x * x`; braces for several statements; parentheses may be dropped for one argument (`x => x * x`). Zero-argument shorthand: `f = {{ 3 }}`.

**Closures:** functions, objects and apply rules cannot see outer-scope variables (except globals) unless declared with `use`: `get_objects(HostGroup).filter((hg) use(name) => hg.name == name)`. A value can be assigned: `use (greeting = "Hello, " + name)`. Parentheses around lambda arguments are required with closures.

**Scopes**, checked in order: local (declared with `var`), `this` (the current object or the object a function was invoked on), global. Use `this.check_interval = 1m` to set the attribute rather than a same-named local; `locals` and `globals` are explicit keywords.

**Conditions:** `if / else if / else` is an expression (null if no branch taken). Ternary: `cond ? a : b`.

**Loops:** `while (cond) {}`; `for (var item in list) {}`; `for (var key => var value in dict) {}`; `break` and `continue` work in both.

**Errors:** `throw "message"`, `try { } except { }`. **Types:** `typeof(3)`; constructors `String(3)`, `PerfdataValue()`. `debugger` inserts a breakpoint (active only with `--script-debugger`).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/17-language-reference/. No commands were run.
