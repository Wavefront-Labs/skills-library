---
id: computing-software.software-engineering.javascript.js-function-parameters-and-arguments
name: js-function-parameters-and-arguments
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-functions, default-parameters, rest-parameters, arguments-object]
level: practitioner
status: docs-checked
description: "Use default, rest and named-object parameters correctly and avoid the arguments object."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Default_parameters", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/arguments", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/Arrow_functions", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Function/length"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Function parameters

- Default parameters apply when no value or `undefined` is passed; they are evaluated at call time, set left to right, and earlier parameters are available to later defaults.
- A rest parameter `...args` collects the remaining arguments as an array. The `arguments` object is array-like (has `length` and indexed properties, not Array methods) and is available in all non-arrow functions. Non-strict functions with only simple parameters sync `arguments` and the parameters.
- `fn.length` counts only the parameters before the first one with a default value and excludes the rest parameter.
- Arrow functions have no own bindings to `this`, `arguments` or `super`, no `new.target`, and calling one with `new` throws a TypeError.
- For many parameters, take one options object with destructuring and defaults: `function f({ retries = 3, signal } = {})`.

## Checked

2026-11-02. Confirmed: MDN Default parameters (undefined, call time, left to right, earlier params), Rest parameters, arguments object (array-like, non-arrow, non-strict sync), Function length, Arrow functions.
Removed: The "null keeps null" example, "fresh default object each call" wording, spread/Math.max argument-limit claim, "about three parameters" rule and return-early advice.
Method: documentation only; no commands were run.
