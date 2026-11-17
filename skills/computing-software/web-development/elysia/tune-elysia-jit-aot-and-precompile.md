---
id: computing-software.web-development.elysia.tune-elysia-jit-aot-and-precompile
name: tune-elysia-jit-aot-and-precompile
category: computing-software
field: web-development
product: elysia
tags: [jit-compiler, sucrose, aot, precompile, performance, trace]
level: sme
status: docs-checked
description: "Understand how Elysia's JIT compiler and Sucrose static analysis work, and decide when to use precompile: true or aot: false."
sources:
  - https://elysiajs.com/internal/jit-compiler.html
  - https://elysiajs.com/patterns/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reason about Elysia's startup and first-request cost and choose the right compile settings.

## How it works

- Elysia has had a JIT "compiler" since 0.4 (in `src/compose.ts`) that uses `new Function(...)`. It generates handler code per route on the first request to that route.
- Sucrose (`src/sucrose.ts`) reads each handler with `Function.toString()` and pattern-matches which request parts it uses. A handler that destructures only `params` makes the generated code parse only params and skip body, query and headers. Traditional frameworks parse everything in a central handler.
- Sucrose is a purpose-built parser for function syntax rather than acorn/esprima because that subset is already formatted by the JS engine; the docs cite lower memory than AST tools.
- Other optimisations: control flow specialised to usage, constant folding, direct property access, `mapCompactResponse` (used when `set` or `status` is not touched, avoiding a full `Response` with custom init).
- On Bun it uses `Bun.serve.routes`, `Bun.websocket`, conditional `Bun.file`, and `Headers.toJSON()`.

## Cost

- First request per route: analysis plus codegen, described as usually under 0.005 ms per route, once per route.
- Generated code is kept in memory (relatively low) and the library is slightly larger.
- Uses `new Function`; the docs argue input is produced by Elysia itself and is almost never user-controlled, as with ajv and TypeBox.

## Settings

```ts
new Elysia({ precompile: true }) // run JIT for all routes before the server starts
new Elysia({ aot: false })       // dynamic mode, no JIT
```

- `precompile: true`: moves the cost to startup (slower start, no first-request overhead). The configuration page recommends leaving it `false`.
- `aot: false`: disables JIT entirely. Not recommended; some features are missing, for example `trace`.

## Gotchas

- Sucrose works from the handler source text, so what the handler visibly reads (e.g. `({ params })`) decides what gets parsed.
- If you rely on `trace`, leave `aot` enabled.

## Checked

2026-11-07. Read in full: internal/jit-compiler (text; the embedded demo component is not documentation text) and patterns/configuration (`aot`, `precompile`). Confirmed the 0.4 JIT origin, Sucrose and `Function.toString()`, the params-only example, optimisations, `mapCompactResponse`, Bun-specific features, the under 0.005 ms per route cost, memory and bundle notes, the `new Function` safety argument, `precompile: true` and `aot: false` (missing features such as `trace`). Removed an OpenTelemetry aside and a note about an unread demo.

Method: documentation only; no commands were run.
