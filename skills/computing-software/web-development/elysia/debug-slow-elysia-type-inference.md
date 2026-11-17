---
id: computing-software.web-development.elysia.debug-slow-elysia-type-inference
name: debug-slow-elysia-type-inference
category: computing-software
field: web-development
product: elysia
tags: [typescript, type-performance, perfetto, eden, tsc-trace, schema-to-type]
level: advanced
status: docs-checked
description: "Diagnose slow TypeScript inference in an Elysia project with a tsc trace in Perfetto, and speed up Eden by exporting a sub app type."
sources:
  - https://elysiajs.com/patterns/typescript.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: find what is slowing editor feedback or triggering "Type instantiation is excessively deep and possibly infinite" in an Elysia codebase.

## Know what is inferred

Elysia infers request and response types from schemas, so manual annotations are rarely needed. This works for TypeBox and Standard Schema libraries: Zod, Valibot, ArkType, Effect Schema, Yup, Joi.

Schema to type:
- TypeBox: `type User = typeof User['static']`
- Zod: `z.infer<typeof User>`
- Valibot: `v.InferOutput<typeof User>`
- ArkType: `typeof User.infer`

## Trace the type checker

1. From the project root:
```bash
tsc --generateTrace trace --noEmit --incremental false
```
This writes a `trace` folder.
2. Open https://ui.perfetto.dev and drag in `trace/trace.json`.
3. In the flame graph, find the long chunk and click it: it shows how long inference took and the file and line it came from.

Elysia runs a local type benchmark before each release, so most projects should not hit problems; use the trace when you do.

## Eden slow? Isolate a sub app

If Eden Treaty inference is slow, expose the type of one plugin instead of the whole app.

```ts
// backend/src/index.ts
const app = new Elysia().use([plugin1, plugin2, plugin3]).listen(3000)
export type app = typeof app
export type subApp = typeof plugin1
```

```ts
// frontend/src/index.ts
import { treaty } from '@elysia/eden'
import type { subApp } from 'backend/src'
const api = treaty<subApp>('localhost:3000')
```

The client then evaluates only that sub app.

## Gotchas

- The sub app trick works because the client then does not need to evaluate the type of the whole app.

## Checked

Checked 2026-11-07 against the Elysia documentation source (patterns/typescript.html); each claim, option name and default was compared with the page text. Removed a filler gotcha.

Method: documentation only; no commands were run.
