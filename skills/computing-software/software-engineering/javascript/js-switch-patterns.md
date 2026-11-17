---
id: computing-software.software-engineering.javascript.js-switch-patterns
name: js-switch-patterns
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, switch-fallthrough, js-control-flow]
level: intro
status: docs-checked
description: "How JavaScript switch works: strict comparison, break and fall-through, one default, shared block scope for let/const, and the switch (true) pattern."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/switch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# switch statements and fall-through

- `switch` finds the first `case` whose expression equals the input using strict equality, then runs all statements from that clause until a `break` or the end. Case expressions are evaluated only until a match is found.
- Without `break`, execution falls through to the next clause, even into `default`, whether or not it matches. `return` (inside a function) and `continue` (inside a loop) also exit the switch.
- A switch may have only one `default`; several give a `SyntaxError`. By convention it is last but need not be: if no case matches, execution starts at `default` and continues from there, falling through any clauses after it.
- No match and no `default`: execution continues after the switch.
- `case` and `default` are labels and create no lexical scope: two `const message` declarations in different cases throw "Identifier 'message' has already been declared". Wrap each case body in braces `case "say_hello": { ... }`.
- Stacked empty cases share one body (`case "Mangoes": case "Papayas":`), the intended use of fall-through.
- `switch (true) { case "fetch" in globalThis: ... }` is an alternative to `if...else` chains that are not `===` comparisons, and it supports intentional fall-through. MDN shows it with predicate calls like `isSquare(shape)`.

Self-check: confirm a forgotten `break` logs both `0` and `1` in the MDN `foo = 0` example.

## Checked

Confirmed against MDN "switch" (page last modified 2025-07-08), read 2026-11-08. Removed: ESLint rule names (`no-fallthrough`, `no-case-declarations`), the TypeScript `never` exhaustiveness tip, the object/`Map` lookup advice and the "easy to misread" opinion; none are on the page.
Method: docs-only read of cited pages, 2026-11-08
