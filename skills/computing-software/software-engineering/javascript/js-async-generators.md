---
id: computing-software.software-engineering.javascript.js-async-generators
name: js-async-generators
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, async-generator, js-async-iteration]
level: advanced
status: docs-checked
description: "Write async function* generators and consume them with for await; know what next() returns and how yielded rejections behave."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function*"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async generators

- `async function* name() { ... }` creates an `AsyncGeneratorFunction`; each call returns a new `AsyncGenerator` that follows the async iterator protocol, and every `next()` call returns a promise resolving to the iterator result object.
- Both `await` and `yield` can be used in the body: it combines async functions with the lazy nature of generators. Async generator functions have no arrow-function counterpart.
- Consume with `for await (const val of foo()) { ... }`; MDN's `foo` yielding `"a"`, `"b"`, `"c"` builds `"abc"`.
- If a yielded promise rejects, the iterator result promise rejects too (`foo().next().catch(...)`), and the `value` of a resolved result is never itself a promise.
- No line terminator is allowed between `async` and `function`; `function` and `*` may be separated by whitespace.
- `async function*` declarations are hoisted like function declarations.

Self-check: with MDN's `foo`, the `for await` loop leaves `str` equal to `"abc"`.

## Checked

Date: 2026-11-03. Confirmed on MDN Statements/async_function*: AsyncGeneratorFunction and AsyncGenerator behaviour, next() promises, await and yield, rejected yield, no arrow form, syntax notes, hoisting, the `for await` example. Removed as not stated there: the paginated fetch example and `yield*`, `break` calling `return()` and `finally` cleanup, queued next() calls, `events.on` from Node, and error surfacing at the loop.

Method: documentation only; no commands were run.
