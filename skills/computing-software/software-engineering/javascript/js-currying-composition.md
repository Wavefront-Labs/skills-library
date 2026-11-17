---
id: computing-software.software-engineering.javascript.js-currying-composition
name: js-currying-composition
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, currying-composition, js-closures-this]
level: practitioner
status: docs-checked
description: "Build small functional helpers with closures: partial application via bind, curry using Function.length, pipe, and the map(parseInt) trap."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/bind", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/length", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/map"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Currying partial application and composition

- Closures let a function keep the data (its lexical environment) of the scope that created it, so a returned function can carry preset arguments.
- Partial application with `bind`: `const addThirtySeven = addArguments.bind(null, 37)` makes a function with a preset first argument; the bound arguments are inserted ahead of any passed at call time, and extra arguments the target ignores stay ignored. `fn.bind(thisArg, a, b)` behaves like `(...rest) => fn.call(thisArg, a, b, ...rest)`.
- Hand-written partial: `const add5 = b => add(5, b)`.
- Curry: `const curry = f => function c(...a) { return a.length >= f.length ? f(...a) : (...b) => c(...a, ...b); }`. `f.length` is the count of parameters before the first default value, destructuring patterns count as one each, and a rest parameter is excluded; so `((a, b = 1, c) => {}).length` is 1 and `((...args) => {}).length` is 0. Curry such functions only after wrapping them in a plain-parameter function.
- Compose: `const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);`. Keep piped functions unary; wrap multi-argument ones.
- Beware `["1","2","3"].map(parseInt)`: `map` passes the element, the index and the array, and `parseInt` takes a radix as its second argument, so the result is `[1, NaN, NaN]` (`parseInt("2", 1)` and `parseInt("3", 2)` are `NaN`).
- Fix with `.map((str) => parseInt(str, 10))` or `.map(Number)`. `Number` also accepts floats and exponent notation, while `parseInt` stops at the first non-integer character.

Self-check: `["1","2","3"].map(parseInt)` gives `[1, NaN, NaN]`; `.map(Number)` gives `[1, 2, 3]`.

## Checked

2026-11-08. Confirmed on MDN Function.prototype.bind (partial application, equivalence to `call`), Function length (default, destructuring, rest rules), Array.prototype.map (the `parseInt` pitfall and both fixes) and the Closures guide. The `curry` and `pipe` one-liners are local recipes built on those documented behaviours, not quoted from the pages. Removed the advice to prefer named steps over point-free chains as unsourced opinion.

Method: docs-only read of cited pages, 2026-11-08
