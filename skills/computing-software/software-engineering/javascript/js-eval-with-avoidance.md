---
id: computing-software.software-engineering.javascript.js-eval-with-avoidance
name: js-eval-with-avoidance
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, no-eval, js-strict-mode]
level: advanced
status: docs-checked
description: "Replace eval and new Function with bracket accessors, callbacks, JSON and Trusted Types; know direct versus indirect eval."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval#never_use_direct_eval!"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoiding eval and new Function

- `eval()` parses and runs a string as a script with the privileges of the caller: an injection sink for XSS. Strict CSP settings forbid `eval()` and the `Function()` constructor. If you must allow it, pass `TrustedScript` objects, enforce Trusted Types with `require-trusted-types-for 'script'` and allow eval with the `'trusted-types-eval'` keyword in `script-src`; `'unsafe-eval'` also allows it but is much less safe because it works even in browsers without Trusted Types.
- Direct eval is a plain `eval(...)` call; everything else (alias variable, member access, `eval?.()`, `(0, eval)(...)`) is indirect. Direct eval sees local scope and inherits strictness; indirect eval runs in global scope, does not inherit strict mode, and `var` declarations in it become globals unless the source has its own `"use strict"`.
- MDN's reasons to avoid direct eval: it runs with the caller's privileges, it is slower, it forces name lookups and defeats engine optimisation, and minifiers give up on scopes that eval can reach.
- `Function(args, body)` also evaluates in global scope without reading local bindings, parses the string as a function body (top-level `return` works), and lets you pass variables as parameters. It is still forbidden under strict CSP.
- Alternatives MDN gives: bracket accessors (`obj[propName]`, or split a path and loop) instead of `eval("obj." + name)`; callbacks (`setTimeout(() => {...}, 1000)`, `addEventListener`) instead of strings; `JSON` for data, noting that JSON syntax is narrower than JavaScript (no trailing commas, quoted keys). Bracket access with unconstrained input can still allow object injection.
- If `eval()` is passed something that is not a string or `TrustedScript`, it returns the argument unchanged (`eval(new String("2 + 2"))` returns the String object).
- In strict mode, declaring or reassigning a variable named `eval` is a `SyntaxError`, and a `with` statement is a `SyntaxError`.

Self-check: search the code for `eval(`, `new Function` and string arguments to `setTimeout`; none remain.

## Checked

Confirmed on the MDN eval page: injection-sink warning, Trusted Types and CSP keywords, direct versus indirect rules, reasons to avoid direct eval, Function() behaviour, bracket accessor, callback and JSON alternatives, non-string argument behaviour, strict-mode rules. Removed: ESLint rule names (`no-eval`, `no-new-func`, `no-implied-eval`), `Map`-of-functions dispatch, expression-parser advice and iframe/worker sandboxing, none of which the page states.

Method: docs-only read of cited pages, 2026-11-08
