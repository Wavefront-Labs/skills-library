---
id: computing-software.software-engineering.javascript.js-error-logging-serialization
name: js-error-logging-serialization
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, error-serialization, js-error-cause]
level: practitioner
status: docs-checked
description: "Wrap errors with Error cause, pick cause vs AggregateError, and serialise errors for reporting."
sources: ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error/cause"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error chaining logging and serialization

- Wrap with context: `throw new Error("Main logic failed", { cause: err })`. `cause` holds the original error passed in `options.cause`; it may be absent.
- `cause` can be any type. Do not assume it is an `Error`, just as the variable in a `catch` clause may not be one. Walk a chain defensively, for example `let e = err; while (e) { log(e.message); e = e.cause; }`, and check types as you go.
- `cause` is a writable, non-enumerable own data property, so any serialiser that copies only enumerable properties will skip it. Build the log object by hand, for example `{ name, message, stack, cause }`, recursing into `cause`.
- Use `cause` for a single failing site that you wrap to add context. Use `AggregateError` for several unrelated failures in one operation, and `SuppressedError` for an error raised while handling another.
- `cause` may carry structured data (for example `{ code: "NonInteger", values: [p, q] }`) for machine parsing, since human-readable messages can be reworded.
- Do not leak stacks or internals to end users; map errors to codes on the server.

Self-check: a two-level error chain appears fully in your log line.

## Checked

2026-11-08. Confirmed on MDN Error cause: the option and property, any-type cause, attributes (writable, non-enumerable, configurable), the cause vs AggregateError vs SuppressedError distinction, and structured-data causes. Removed claims about how Node and browser consoles print causes, and the source-map and error-tracker grouping advice, which the page does not cover.

Method: docs-only read of cited pages, 2026-11-08
