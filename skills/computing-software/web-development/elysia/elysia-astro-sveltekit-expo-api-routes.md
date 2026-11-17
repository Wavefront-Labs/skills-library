---
id: computing-software.web-development.elysia.elysia-astro-sveltekit-expo-api-routes
name: elysia-astro-sveltekit-expo-api-routes
category: computing-software
field: web-development
product: elysia
tags: [integrations-frameworks, astro, sveltekit, expo, wintertc]
level: practitioner
status: docs-checked
description: "Host Elysia in Astro endpoints, SvelteKit server routes or Expo API routes, with the right file name, exported handler and prefix for each."
sources:
  - https://elysiajs.com/integrations/astro.html
  - https://elysiajs.com/integrations/sveltekit.html
  - https://elysiajs.com/integrations/expo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run an Elysia app as the API layer of Astro, SvelteKit or Expo Router. Elysia works because it follows WinterTC (web-standard Request/Response).

Astro:
1. Set `output: 'server'` in the Astro config module (the `mjs` file passed to defineConfig) (`defineConfig({ output: 'server' })`).
2. Create `pages/[...slugs].ts`:

```typescript
const app = new Elysia().get('/api', () => 'hi')
    .post('/api', ({ body }) => body, { body: t.Object({ name: t.String() }) })
const handle = ({ request }: { request: Request }) => app.handle(request)
export const GET = handle
export const POST = handle
```

Astro on Bun is recommended but not required.

SvelteKit:
1. Create `src/routes/[...slugs]/+server.ts`.
2. Export a `fallback` (not GET/POST) that calls `app.handle`:

```typescript
export const fallback = ({ request }: { request: Request }) => app.handle(request)
```

Expo (SDK 50+, App Router v3):
1. Create `app/[...slugs]+api.ts`, define the app and `export const GET = app.fetch; export const POST = app.fetch`.

Prefix rule (all three): if the file is not at the router root, set `new Elysia({ prefix })` to the folder, e.g. `pages/api/[...slugs].ts`, `src/routes/api/[...slugs]/+server.ts` or `app/api/[...slugs]+api.ts` all need `prefix: '/api'`.

pnpm: `pnpm add @sinclair/typebox openapi-types`.

Expo Eden: `export type app = typeof app` from the API file, then `treaty<app>('localhost:3000/api')` in `lib/eden.ts`. Deployment: deploy as a normal Elysia app, or use the experimental Expo server runtime: `expo export` produces a function at `dist/server/_expo/functions/[...slugs]+api.js`, which Expo treats as an Edge function (it allocates no port). Expo adapters: Express, Netlify, Vercel.

Gotchas:
- SvelteKit exports `fallback`; Astro and Expo export method-named handlers (`GET`, `POST`).
- Expo's Eden sample shows `treaty.schema` for the body; the other samples on these pages use `t.Object`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/astro.html, integrations/sveltekit.html, integrations/expo.html); each claim, option name and default was compared with the page text. Removed an invented Verify step, an unsupported Next claim and speculation about a docs slip.

Method: documentation only; no commands were run.
