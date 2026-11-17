---
id: computing-software.software-engineering.nim.dom-asyncjs-and-promises
name: dom-asyncjs-and-promises
category: computing-software
field: software-engineering
product: nim
tags: [dom-asyncjs-and-promises, jsffi-and-js-stdlib, dom, asyncjs, promise, async-js, fetch, events, browser-api, jsconsole, nim]
level: practitioner
status: docs-checked
description: "Use std/dom for browser APIs and std/asyncjs {.async.} procs that compile to JavaScript async functions and promises."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/lib/js/dom.nim
  - https://github.com/nim-lang/Nim/blob/devel/lib/js/asyncjs.nim
  - https://github.com/nim-lang/Nim/blob/devel/lib/js/jsconsole.nim
  - https://github.com/nim-lang/Nim/blob/devel/doc/backends.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# dom, asyncjs and Promises

Goal: write browser code in Nim.

- Compile with `nim js file.nim`; the default output is a `.js` file referenced from an `.html` page (`nim js -o:calculator.js calculator.nim`). `nim js -r` runs the code with Node.js (use a recent Node: at least 12.0 if `globalThis` is reported undefined).
- `import std/dom` declares the DOM for the JS backend (the module errors on other backends). It provides `document`, `window`, `setTimeout(action, ms)` and handler fields such as `onclick`.
- `document.querySelector(selectors: cstring)` returns an `Element`; `document.createElement(identifier: cstring)`; `innerHTML` is a `cstring` field; `appendChild`.
- Events: `document.addEventListener("DOMContentLoaded", proc(e: Event) = ...)`; the module docs also name `"load"`, `"unload"` and `"beforeunload"`. Handlers are `proc(ev: Event)`.
- `import std/jsconsole` gives `console.log(...)`, `console.error`, `console.warn` and more (varargs, styled `%c` messages).
- `import std/asyncjs`: a proc is asynchronous when it carries `{.async.}` and returns `Future[T]` (or nothing, which means `Future[void]`). This is roughly the JS `async` keyword; call it with `await`: `var game = await loadGame(name)`. Forward declarations need `{.async.}` too.
- Wrap callback APIs with `newPromise`. `then` and `catch` exist on `Future[T]` for newer versions (since 1.5.1).
- Nim emits `async/await` JavaScript, supported by modern browsers, Node.js and Electron; use a backporting tool such as babel for older runtimes.

Gotchas:
- `std/asyncjs` needs the JS backend and is designed for it only.
- The JS backend lacks `cast`, `zeroMem`, file management, threading, coroutines and some stdlib modules.
- Not every browser API is wrapped; fall back to `std/jsffi` for the rest.

Verify: clicking a button updates text on the page.

## Checked

2026-11-08. Read in full: lib/js/asyncjs.nim, lib/js/jsconsole.nim (first 60 lines plus the `console` declaration), the backends.md JS-target section (searched by section). lib/js/dom.nim was searched by symbol and its header documentation read (large 55 KB file, not read end to end). Removed: the `std/jsfetch` and fetch-binding advice (not confirmed in the files read), the closure-capture gotcha, and the `-d:release` and `window.onload` advice (the docs use `DOMContentLoaded`); tut1, manual and lib.html dropped from sources.
Method: documentation only; no commands were run.
