---
id: computing-software.software-engineering.javascript.js-default-rest-params
name: js-default-rest-params
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, rest-parameters, js-functions]
level: practitioner
status: docs-checked
description: "Rest parameter syntax rules, how rest differs from the arguments object, and its effect on function length."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rest parameters

- A function's last parameter can be prefixed with `...`; all remaining user-supplied arguments are placed in an Array. With `function myFun(a, b, ...manyMoreArgs)`, calling `myFun("one", "two")` gives `[]`; with one extra argument it gives a one-element array.
- Syntax rules: only one rest parameter, it must be last, no trailing comma after it, and it cannot have a default value (`function wrong4(...wrong = []) {}` is a syntax error).
- The rest parameter may be destructured: `function ignoreFirst(...[, b, c])`.
- The rest parameter is not counted towards the function's `length`.
- Rest versus `arguments`: rest is a real Array (so `sort()`, `map()`, `forEach()`, `pop()` work), `arguments` is not (`arguments.sort` throws a `TypeError`); `arguments` has the deprecated `callee`; in a non-strict function with simple parameters `arguments` syncs with re-assigned named parameters while the rest array never updates; rest excludes the named parameters before it, `arguments` contains all of them.
- If the only parameter is a rest parameter, `restParams.length` equals `arguments.length`.
- Rest parameters replace `Array.prototype.slice.call(arguments)` and `Array.from(arguments)` boilerplate. MDN marks them Baseline widely available since September 2016.

Self-check: `fun1()` prints 0, `fun1(5)` prints 1, `fun1(5, 6, 7)` prints 3.

## Checked

Confirmed against MDN "Rest parameters" (page last modified 2025-07-08), read 2026-11-08. Removed: default-parameter claims (`undefined` vs `null`, per-call evaluation, `fn.length` before a default), options-object destructuring pattern, `Object.hasOwn` advice and the arrows-have-no-arguments note; those belong to the Default parameters page, which this skill does not cite.
Method: docs-only read of cited pages, 2026-11-08
