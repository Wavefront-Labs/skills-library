---
id: computing-software.software-engineering.javascript.js-sloppy-mode-this-globals
name: js-sloppy-mode-this-globals
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, implicit-globals, js-strict-mode]
level: practitioner
status: docs-checked
description: "Catch accidental globals and sloppy-mode this coercion; enable strict mode everywhere."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implicit globals and this in sloppy mode

- Assigning to an undeclared name creates a property on the global object in sloppy mode; in strict mode it throws a `ReferenceError`. To set a global on purpose, assign to a property of `globalThis`.
- A plain call `f()` gets the global object as `this` in sloppy mode and `undefined` in strict mode. Sloppy mode also boxes a primitive `this` (and replaces `undefined`/`null` with the global object); strict mode passes the value unchanged.
- Strict mode also makes these syntax errors: duplicate parameter names, legacy `0`-prefixed octal literals (use `0o`), the `with` statement, `delete` on a plain variable name, and binding or assigning `eval`/`arguments`. It throws on `arguments.callee` and on assigning to read-only properties.
- ES modules and class bodies are always strict. In a script, the exact statement `"use strict";` must come before any other statements, in the script or in a function body.
- `"use strict"` inside a function with default, rest or destructured parameters is a syntax error.
- The directive does not apply to a block in `{}` braces.
- In strict mode `arguments` is not linked to named parameters: assigning to one does not change the other.
- Migration can be gradual, per file or per function: add the directive, fix the syntax errors, then test for the new runtime errors.

Self-check: `(function(){ "use strict"; undeclared = 1; })()` throws a `ReferenceError`.

## Checked

2026-11-08. Confirmed against the MDN Strict mode page: undeclared assignment, `this` handling and boxing, the list of syntax errors, module and class strictness, directive placement and the simple-parameters restriction, `arguments` not syncing, and gradual migration. Removed the ESLint rule names (`no-undef`, `no-implicit-globals`), which that page does not cover.

Method: docs-only read of cited pages, 2026-11-08
