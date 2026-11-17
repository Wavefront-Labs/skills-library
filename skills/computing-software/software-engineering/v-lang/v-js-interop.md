---
id: computing-software.software-engineering.v-lang.v-js-interop
name: v-js-interop
category: computing-software
field: software-engineering
product: v-lang
tags: [v-js-interop, javascript-backend, js interop, js, promise, dom, fn js, async await, js types, window, v-lang]
level: advanced
status: draft
description: "Call JavaScript from V with the JS. namespace, declare external functions and types, and handle promises and DOM objects."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# JS interop: JS. namespace, async and DOM

Goal: use JS libraries from V code.

- Declare externals: `fn JS.alert(msg string)`, `fn JS.console.log(s JS.Any)`; types `JS.Any`, `JS.String`, `JS.Number`, `JS.Object`, `JS.Promise` (confirm names in `vlib/builtin/js`).
- Use directly: `JS.document.getElementById('x'.str)`... (call patterns vary by version; confirm with examples in the repo's `examples/js_hello_world`).
- Inline JS: `#js` or `$js` pragmas / `JS.eval` style helpers (confirm availability).
- Promises: `fn (p JS.Promise) then(...)`; async function support via `await` keyword on JS promises (confirm).
- Export a function for host JS: `@[export: 'greet']` (confirm).

Gotchas:
- Strings convert to JS strings through `.str` helper conversions; verify with a runtime test.
- Not all V types map cleanly (structs become objects, maps become Map or objects depending on version).

Verify: compile a page calling `JS.alert` and open it in a browser.
