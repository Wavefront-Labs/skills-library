---
id: computing-software.software-engineering.javascript.js-destructuring-and-spread
name: js-destructuring-and-spread
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-destructuring, spread-operator, object-rest, shallow-copy]
level: practitioner
status: docs-checked
description: "Destructure arrays and objects with defaults, renaming and rest, and know spread copies are shallow."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Destructuring

- Object: `const { a, b: renamed = 5, ...rest } = obj;` Array: `const [first, , third, ...others] = arr;` Array rest collects the remaining iterable elements into a new array.
- Non-iterables cannot be destructured as arrays.
- A default is used when the property is missing or `undefined`; it is not used for `null`.
- Computed property names work in destructuring: `const { [key]: value } = obj`.
- Swapping variables: `[a, b] = [b, a]` (needs a leading semicolon on the previous line if you omit semicolons).

## Checked

Date: 2026-11-02. Confirmed on MDN (Operators/Destructuring): object/array/rest forms, non-iterable error, defaults only for undefined, computed names, swapping. Removed as not stated there: spread semantics (own enumerable, getters, shallow), ES2018 dating, the TypeError on null/undefined, argument-limit overflow and structuredClone advice (not on this page).

Method: documentation only; no commands were run.
