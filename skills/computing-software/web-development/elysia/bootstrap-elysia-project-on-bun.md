---
id: computing-software.web-development.elysia.bootstrap-elysia-project-on-bun
name: bootstrap-elysia-project-on-bun
category: computing-software
field: web-development
product: elysia
tags: [elysia, bun, quick-start, scaffold, typescript]
level: intro
status: docs-checked
description: "Create a new Elysia server on Bun, either with bun create elysia or by hand, with the dev, build, start and test scripts and strict TypeScript."
sources:
  - https://elysiajs.com/quick-start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a running Elysia server on Bun that reloads on file change and builds for production.

## Automatic setup

```bash
bun create elysia app
cd app
bun dev
```

Open localhost:3000; it should greet you with "Hello Elysia". The generated `dev` command auto-reloads the server on file changes.

## Manual setup

```bash
bun add elysia
bun add -d @types/bun
```

Create `src/index.ts`:

```typescript
import { Elysia } from 'elysia'

const app = new Elysia()
	.get('/', () => 'Hello Elysia')
	.listen(3000)

console.log(`Elysia is running at ${app.server?.hostname}:${app.server?.port}`)
```

Add scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "bun --watch src/index.ts",
    "build": "bun build src/index.ts --target bun --outdir ./dist",
    "start": "NODE_ENV=production bun dist/index.js",
    "test": "bun test"
  }
}
```

- dev: development with auto-reload on code change.
- build: bundle for production into `./dist`.
- start: run the production server from the built file.

## TypeScript

If you use TypeScript, set `compilerOptions.strict` to `true` in `tsconfig.json`, as the quick start instructs.

## Verify

Run `bun dev` and open localhost:3000; it should greet you with "Hello Elysia".

## Gotchas

- Elysia is optimised for Bun but not limited to it; use the Node.js or web-standard skills for other runtimes.
- Without TypeScript you may miss auto-completion, advanced type checking and end-to-end type safety (the quick start warns about this).

## Checked

Checked 2026-11-07 against the Elysia documentation source (quick-start.html); each claim, option name and default was compared with the page text. Removed the claim that strict is required for inference, the app.server verify sentence and the at-glance source.

Method: documentation only; no commands were run.
