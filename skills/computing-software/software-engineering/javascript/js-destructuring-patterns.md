---
id: computing-software.software-engineering.javascript.js-destructuring-patterns
name: js-destructuring-patterns
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, nested-destructuring, js-destructuring]
level: practitioner
status: docs-checked
description: "Destructure nested objects and arrays with defaults, renaming, rest and computed keys; know the null and undefined TypeError."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested destructuring patterns

- Rename and default: `const { a: x = 1, b: { c } = {} } = obj;`. A default applies when the property is missing or `undefined`, not when it is `null`; the default expression is evaluated only when needed.
- Arrays: `const [first, , third, ...rest] = arr;`. Missing elements give `undefined`. Array destructuring uses the iterable protocol, so any iterable (a `Map`, a generator) works and is only iterated until all bindings are filled; a non-iterable throws `TypeError`. The rest binding is evaluated eagerly into a new array.
- Rest: `...rest` must be last and cannot have a trailing comma. It makes a shallow copy (no deep copy). In objects it copies the remaining enumerable own properties and must be an identifier; in arrays it can itself be a pattern (`...[c, d]`).
- Swap: `[a, b] = [b, a];`.
- Computed key: `const { [key]: v } = obj;`. Non-identifier keys need renaming: `const { "fizz-buzz": fizzBuzz } = foo;`.
- Works in function parameters (give the whole pattern a default, `= {}`, if the function may be called with no argument) and in `for...of`, `for...in` and `catch` bindings.
- Assignment without a declaration needs parentheses: `({ a, b } = obj);`. If your style omits semicolons, precede that line with one.
- Destructuring `null` or `undefined` throws `TypeError`, even with an empty pattern (`const {} = null`). A primitive is wrapped, so `const { toFixed } = 1` works. Object destructuring also looks up the prototype chain.
- Binding patterns share one declaration keyword; destructure twice (`const` and `let`) if some variables must be re-assignable.

Self-check: `const { a: { b } } = {}` throws `TypeError`; `const { a: { b } = {} } = {}` does not.

## Checked

Confirmed on the MDN Destructuring page: defaults and the null rule, rest rules, iterable behaviour, swap, computed and non-identifier keys, parameter defaults, parentheses and semicolon note, TypeError cases, prototype lookup and binding-versus-assignment patterns. Removed: the "over-deep patterns hurt readability" advice, which is an opinion the page does not state.

Method: docs-only read of cited pages, 2026-11-08
