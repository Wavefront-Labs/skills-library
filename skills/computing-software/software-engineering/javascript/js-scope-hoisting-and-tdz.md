---
id: computing-software.software-engineering.javascript.js-scope-hoisting-and-tdz
name: js-scope-hoisting-and-tdz
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-scope, hoisting, temporal-dead-zone, var-let-const]
level: practitioner
status: docs-checked
description: "Predict hoisting, the temporal dead zone and block scope for var, let, const and function declarations."
sources: ["https://tc39.es/ecma262/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/let", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/var", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/const"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scope, hoisting and the TDZ

- `var` declares function-scoped or globally-scoped variables; declarations are processed before any code runs, so a `var` can be used before its line and reads as `undefined` (default value `undefined`).
- `let` and `const` are block-scoped and can only be accessed after the place of declaration is reached; before that they are in the temporal dead zone (TDZ). The same applies to `class` declarations.
- `const` stops reassignment of the binding; it does not make the value immutable.
- Assigning to an undeclared name creates a property on the global object in sloppy mode and throws an error in strict mode.
- Prefer `const` by default, `let` when reassigned, and avoid `var`.

## Checked

2026-11-02. Confirmed: MDN let (block scope, TDZ for let/const/class), var (function scope, hoisting, default undefined), const (no reassignment), Strict mode (undeclared assignment throws).
Removed: Function-declaration hoisting and block-function legacy rules, per-iteration loop binding claim, ESLint rule names and the ReferenceError wording (not stated on the pages read).
Method: documentation only; no commands were run.
