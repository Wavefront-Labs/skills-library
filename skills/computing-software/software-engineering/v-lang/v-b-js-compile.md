---
id: computing-software.software-engineering.v-lang.v-b-js-compile
name: v-b-js-compile
category: computing-software
field: software-engineering
product: v-lang
tags: [v-b-js-compile, javascript-backend, -b js, javascript backend, js_node, js_browser, js_freestanding, transpile, node, v-lang]
level: practitioner
status: docs-checked
description: "Compile V to JavaScript with v -b js, enable source maps, split code into .js.v files and test for js_node, js_browser and js_freestanding."
sources:
  - https://github.com/vlang/v/blob/master/doc/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compiling V to JavaScript with -b js

Goal: target the JS backend.

- Build: `v -b js -sourcemap hello.v -o hello.js`. The `-sourcemap` flag activates source maps so the generated JavaScript can be debugged; the docs list `v help build-js` for all supported options.
- Files named `*.js.v` are compiled only by the JS backend and may contain JS code; `*.c.v` files are C-backend only and `*.native.v` files are native-backend only.
- Compile-time conditions: `$if js { }` is a builtin option; `js_node`, `js_browser` and `js_freestanding` are also listed among the builtin `$if` options.

Gotchas:
- Check `v help build-js` for the exact flags of your version; this skill does not list the target-selection flags.
- Code behind `$if js` or in `.js.v` files is not compiled for other backends, so keep a fallback.

Verify: `v -b js -sourcemap hello.v -o hello.js` produces `hello.js`.

## Checked

2026-11-08. Read: the "Javascript Backend", "Environment specific files" and builtin-options table sections of doc/docs.md (vlang/v). Removed unconfirmed claims: `-b js_node`/`-b js_browser`/`-b js_freestanding` as build targets, the stdlib subset, Promise mapping, BigInt handling, `JS.console.log`, single-script output and integer overflow notes. docs.vlang.io (script-rendered) and modules.vlang.io dropped from sources.
Method: documentation only; no commands were run.
