---
id: computing-software.software-engineering.javascript.js-control-flow-loops-and-labels
name: js-control-flow-loops-and-labels
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-control-flow, for-of-vs-for-in, switch-fallthrough, labeled-break]
level: intro
status: gated
description: "Pick the right loop and avoid for-in, switch fallthrough and early-exit mistakes."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control flow

- `for...of` iterates values of any iterable (arrays, strings, Maps, Sets, generators); `for...in` iterates enumerable string keys including inherited ones: never use it on arrays. `for await...of` consumes async iterables.
- `break` and `continue` can target a label: `outer: for (...) { for (...) { continue outer; } }`. `forEach` and `map` callbacks cannot `break`; use `for...of`, `some` or `every`.
- `switch` uses strict equality and falls through without `break`; wrap each case body in braces when declaring `let`/`const`. Use `default` last and return in each case in a function.
- Truthiness: falsy values are `false, 0, -0, 0n, "", null, undefined, NaN` (and `document.all`). Empty arrays and objects are truthy.
- `try...finally` runs `finally` even after `return`; a `return` in `finally` overrides everything and swallows exceptions.
- Comma, `void`, and `==` have surprising behaviour: lint with `eqeqeq`.

## Checked

- Date: 2026-11-02.
- Source pages listed in `sources` were fetched where possible; ECMA-262 (too large to read) and the MDN landing page only; falsy list and eqeqeq advice not checked. Treat the specific names, flags and figures as unconfirmed (gated: unconfirmed, source is paywalled or blocked).

Method: documentation only; no commands were run.
