---
id: computing-software.software-engineering.javascript.js-strict-mode-and-sloppy-pitfalls
name: js-strict-mode-and-sloppy-pitfalls
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, js-strict-mode, use-strict, sloppy-mode, this-undefined]
level: practitioner
status: docs-checked
description: "Know what strict mode changes and where it is on by default."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Strict_mode"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strict mode

- Enabled by `"use strict"` before any other statement in a script or function; JavaScript modules are strict automatically.
- Changes include: assignment to undeclared variables throws, legacy octal literals are errors, and `eval` and `arguments` are simplified.
- The `"use strict"` directive cannot be used in a function with non-simple parameters (default, rest or destructured).
- Migrate legacy code by enabling it per file and fixing thrown errors; add ESLint `strict` or use modules.

## Checked

Date: 2026-11-02. Confirmed on MDN (Strict_mode): directive placement, modules strict, undeclared assignment, legacy octal, eval/arguments, non-simple parameters rule. Removed as not stated there: this-in-plain-calls, with, duplicate parameters, class bodies and concatenation advice (not read).

Method: documentation only; no commands were run.
