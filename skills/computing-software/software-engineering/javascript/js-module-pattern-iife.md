---
id: computing-software.software-engineering.javascript.js-module-pattern-iife
name: js-module-pattern-iife
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, iife-pattern, js-scope]
level: intro
status: docs-checked
description: "Use IIFEs for a private scope, async context or multi-statement value; know when parentheses are needed."
sources: ["https://developer.mozilla.org/en-US/docs/Glossary/IIFE"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IIFE and module-pattern encapsulation

- An IIFE (Immediately Invoked Function Expression) is a function that runs as soon as it is defined. Forms: `(function () { ... })();`, the arrow variant `(() => { ... })();` and the async variant `(async () => { ... })();`.
- It has two parts: a function expression, which usually needs enclosing parentheses to parse correctly, and an immediate call (arguments are allowed, though IIFEs without arguments are more common).
- Documented uses: avoid polluting the global namespace by creating a new scope; create an async context to use `await` where the surrounding code is not async; compute a value with multiple statements in a place that needs a single expression.
- Classic module pattern: `const counter = (() => { let n = 0; return { inc: () => ++n }; })();` keeps `n` private and exposes only `inc`.
- An IIFE is more powerful than the comma operator, which can only run multiple expressions and cannot use local variables or control flow.

Self-check: `typeof n` outside the IIFE is `"undefined"`.

## Checked

2026-11-08. Confirmed on the MDN IIFE glossary page: the three forms, the two parts, the use cases and the comma-operator comparison. Removed the claims about leading semicolons and ASI, top-level `var` creating `window` properties, and preferring blocks or ES modules, which that page does not state.

Method: docs-only read of cited pages, 2026-11-08
