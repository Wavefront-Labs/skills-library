---
id: computing-software.web-development.elysia.elysia-run-on-node-or-deno
name: elysia-run-on-node-or-deno
category: computing-software
field: web-development
product: elysia
tags: [integrations-deploy, node, deno, adapter, runtime]
level: practitioner
status: docs-checked
description: "Run Elysia outside Bun: the @elysia/node adapter for Node.js with tsx scripts, or Deno.serve with app.fetch for Deno."
sources:
  - https://elysiajs.com/integrations/node.html
  - https://elysiajs.com/integrations/deno.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run an Elysia app on Node.js or Deno.

Node.js:
1. Install the adapter with your package manager: `bun add elysia @elysia/node` (also `pnpm add`, `npm install`, `yarn add`).
2. Apply it on the main instance:

```typescript
import { Elysia } from 'elysia'
import { node } from '@elysia/node'

const app = new Elysia({ adapter: node() })
    .get('/', () => 'Hello Elysia')
    .listen(3000)
```

3. Optional dev setup: `npm install --save-dev tsx @types/node typescript`, then package.json scripts:

```json
{ "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc src/index.ts --outDir dist",
    "start": "NODE_ENV=production node dist/index.js" } }
```

Run `tsc --init` and set `compilerOptions.strict` to `true`. `dev` gives auto-reload, `build` compiles for production, `start` runs it.

Deno:
1. Drop `.listen(3000)` and wrap the fetch handler:

```typescript
const app = new Elysia().get('/', () => 'Hello Elysia')
Deno.serve(app.fetch)
```

2. Run with `deno serve --watch src/index.ts`.
3. Change port with `Deno.serve({ port: 8787 }, app.fetch)`.

pnpm (both runtimes): `pnpm add @sinclair/typebox openapi-types`.

Gotchas:
- The Node setup depends on passing `adapter: node()` to the main Elysia instance.
- On Deno the docs show removing `.listen()`; keeping it is not what the page demonstrates.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/node.html, integrations/deno.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
