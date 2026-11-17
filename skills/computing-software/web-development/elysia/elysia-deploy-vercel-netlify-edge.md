---
id: computing-software.web-development.elysia.elysia-deploy-vercel-netlify-edge
name: elysia-deploy-vercel-netlify-edge
category: computing-software
field: web-development
product: elysia
tags: [integrations-deploy, vercel, netlify, edge-functions, deployment]
level: practitioner
status: docs-checked
description: "Deploy Elysia to Vercel Functions (Node or Bun runtime) or Netlify Edge Functions by default-exporting the app, with required config files."
sources:
  - https://elysiajs.com/integrations/vercel.html
  - https://elysiajs.com/integrations/netlify.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship an Elysia app to Vercel or Netlify with minimal config.

Vercel (zero configuration, Bun or Node runtime):
1. In `src/index.ts` default-export the app:

```typescript
import { Elysia, t } from 'elysia'

export default new Elysia()
    .get('/', () => 'Hello Vercel Function')
    .post('/', ({ body }) => body, { body: t.Object({ name: t.String() }) })
```

2. Develop locally with `vc dev`; deploy with `vc deploy`.
3. Node runtime: set `"type": "module"` in package.json.
4. Bun runtime: set `"bunVersion": "1.x"` in `vercel.json` (with `"$schema": "https://openapi.vercel.sh/vercel.json"`).
5. Further settings are in the Vercel docs page for Elysia.

Netlify Edge Functions (these run on Deno, which Elysia supports):
1. Functions live in `netlify/edge-functions` by default. To serve `/hello`, create `netlify/edge-functions/hello.ts`:

```typescript
import { Elysia } from 'elysia'

export const config = { path: '/hello' }

export default new Elysia({ prefix: '/hello' })
    .get('/', () => 'Hello Elysia')
```

2. Local testing: `bun add -g netlify-cli` then `netlify dev`.

pnpm on either: `pnpm add @sinclair/typebox openapi-types` because pnpm does not auto-install peer dependencies.

Gotchas:
- The Netlify example sets `config.path` and the Elysia `prefix` to the same `/hello`.
- Neither example calls `.listen()`; both default-export the Elysia instance.
- The Vercel `package.json` and `vercel.json` snippets are labelled `ts` in the docs but are JSON.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/vercel.html, integrations/netlify.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.
