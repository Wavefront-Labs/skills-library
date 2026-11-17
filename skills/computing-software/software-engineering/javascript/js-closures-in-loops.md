---
id: computing-software.software-engineering.javascript.js-closures-in-loops
name: js-closures-in-loops
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, loop-closure-capture, js-scope]
level: practitioner
status: docs-checked
description: "Fix the classic var-in-loop closure bug with let/const, for...of, forEach, a factory function or an IIFE."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Closures"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Closures captured in loops

- Blocks with curly braces do not create a scope for `var`; a `var` loop variable (or a `var item` inside the loop body) has function scope due to hoisting, so every closure created in the loop shares one lexical environment.
- The callbacks read the variable when they run, after the loop has finished, so they all see the last value. MDN's example: every `onfocus` handler shows the last help text (the age field) because `item` points at the last array entry.
- Fix 1, `let`/`const`: `for (let i = 0; ...) { const item = helpText[i]; ... }` gives each closure its own block-scoped binding, so no extra closures are needed.
- Fix 2, `for...of` with `const item`, or `helpText.forEach((item) => ...)`: both avoid the problem.
- Fix 3, a function factory: `makeHelpCallback(help)` returns a function and creates a new lexical environment for each callback.
- Fix 4, an anonymous closure (IIFE) inside the loop body that declares `var item` locally.
- Do not create functions inside other functions unless you need the closure; each function instance manages its own scope, which costs processing speed and memory. Put methods on the prototype rather than in the constructor.

Self-check: wire up three handlers with `var` and with `let`; with `var` every handler reports the last item.

## Checked

2026-11-08. Confirmed on the MDN Closures guide, section "Creating closures in loops: A common mistake" and "Performance considerations". Removed the `setTimeout` `3 3 3` versus `0 1 2` prediction and the "large unused variables stay alive" claim, which the page does not state.

Method: docs-only read of cited pages, 2026-11-08
