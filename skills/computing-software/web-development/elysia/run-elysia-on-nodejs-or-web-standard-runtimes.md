---
id: computing-software.web-development.elysia.run-elysia-on-nodejs-or-web-standard-runtimes
name: run-elysia-on-nodejs-or-web-standard-runtimes
category: computing-software
field: web-development
product: elysia
tags: [elysia, quick-start, nodejs, web-standard, adapter, fetch]
level: practitioner
status: docs-checked
description: "Run Elysia outside Bun using the @elysia/node adapter with tsx, or export app.fetch for any runtime that supports Web Standard Request and Response."
sources:
  - https://elysiajs.com/quick-start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: host an Elysia app on Node.js, or on any WinterTC / Web Standard runtime.

## Node.js (TypeScript)

```bash
npm install elysia @elysia/node
npm install --save-dev tsx @types/node typescript
npx tsc --init
```

With pnpm, peer dependencies are not installed, so also add `@sinclair/typebox openapi-types`.

`src/index.ts`:

```typescript
import { Elysia } from 'elysia'
import { node } from '@elysia/node'

const app = new Elysia({ adapter: node() })
	.get('/', () => 'Hello Elysia')
	.listen(3000, ({ hostname, port }) => {
		console.log(`Elysia is running at ${hostname}:${port}`)
	})
```

Scripts:

```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc src/index.ts --outDir dist",
    "start": "NODE_ENV=production node dist/index.js"
  }
}
```

Set `compilerOptions.strict` to `true` in `tsconfig.json`.

## Node.js (JavaScript)

Same packages minus the TypeScript tooling, file `src/index.js`, and `"type": "module"` in `package.json` with `dev` as `node src/index.js`. The docs warn you lose auto-completion, advanced type checking and end-to-end type safety without TypeScript.

## Web Standard runtimes

Elysia is WinterTC compliant: anything that supports Web Standard Request/Response can run it. Install only `elysia` (plus the pnpm peers above). The docs list Cloudflare Worker, Next.js, Expo, Astro, Nuxt, SvelteKit and Tanstack Start integrations. For an unlisted runtime, hand it `app.fetch`:

```typescript
const app = new Elysia().get('/', () => 'Hello Elysia').listen(3000)

export default app.fetch
```

## Gotchas

- On Node the adapter must be passed to the constructor: `new Elysia({ adapter: node() })`.
- Node's `listen` takes a callback receiving `{ hostname, port }`; on Bun you read `app.server` instead.

## Checked

2026-11-07. Read in full: quick-start (Bun, Node.js TypeScript and JavaScript, and Web Standard tabs). Confirmed the `npm install` and `tsx` commands, the pnpm peer dependency note (`@sinclair/typebox openapi-types`), `new Elysia({ adapter: node() })`, the `listen` callback with `{ hostname, port }`, the three scripts, `npx tsc --init`, `compilerOptions.strict`, the JavaScript variant (`"type": "module"`, `dev` as `node src/index.js`), the TypeScript-loss warning, the WinterTC wording, the seven listed integrations and `export default app.fetch`. Nothing removed.

Method: documentation only; no commands were run.
