---
id: computing-software.software-engineering.javascript.js-static-blocks-accessors
name: js-static-blocks-accessors
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, static-initialization-blocks, js-class-fields]
level: advanced
status: docs-checked
description: "Use class static initialization blocks for setup that needs private static access; know their order and scope."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/Static_initialization_blocks", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/new.target"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static initialization blocks

- `static { ... }` blocks run during class evaluation. A class can have any number of them; they are evaluated in declaration order together with interleaved static field initializers. A superclass's static initialization runs before its subclasses'.
- They can access private static fields, which initialization logic outside the class cannot, and avoid exposing an `init()` method just for setup.
- Variables declared in a block (`var`, `function`, `const`, `let`) are local to it; `var` is not hoisted out of the block.
- `this` inside a block is the class (MDN: `this.staticProperty2 = "Property 2"`), and `new.target` is `undefined`.

Self-check: log inside a static block; it prints once at class evaluation, before any instance exists.

## Checked

Date: 2026-11-03. Confirmed on MDN Classes/Static_initialization_blocks and Operators/new.target: block count and ordering, superclass-first order, private static access, block scope, `this` in a block, `new.target`. Removed as not stated in the pages read: get/set accessor placement, field initialiser timing and define semantics, arrow-field memory cost, the try/catch use case; the title and description no longer mention accessors.

Method: documentation only; no commands were run.
