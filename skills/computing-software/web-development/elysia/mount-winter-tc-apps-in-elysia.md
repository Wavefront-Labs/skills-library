---
id: computing-software.web-development.elysia.mount-winter-tc-apps-in-elysia
name: mount-winter-tc-apps-in-elysia
category: computing-software
field: web-development
product: elysia
tags: [mount, wintertc, hono-interop, fetch-handler, request-response]
level: practitioner
status: docs-checked
description: "Use Elysia .mount() to attach any Request/Response fetch handler such as a Hono app under a path, or mount Elysia inside another framework."
sources:
  - https://elysiajs.com/patterns/mount.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run another WinterTC-compliant framework inside Elysia (or the reverse) in one process.

## Background

WinterTC servers use the Web Standard `Request` and `Response`, so they interoperate across runtimes. Elysia is WinterTC compliant (optimised for Bun, usable elsewhere).

## Mount a fetch function

`.mount(path, fetch)` takes any function that receives a `Request` and returns a `Response`:

```ts
import { Elysia } from 'elysia'
import { Hono } from 'hono'

const hono = new Hono().get('/', (c) => c.text('Hello from Hono!'))

const app = new Elysia()
  .get('/', () => 'Hello from Elysia')
  .mount('/hono', hono.fetch)
```

`GET /hono` is answered by Hono; `GET /` by Elysia.

## Mount Elysia in another framework

If the other framework has its own `.mount`, pass `elysia.fetch`:

```ts
const elysia = new Elysia().get('/', () => 'Hello from Elysia inside Hono inside Elysia')
const hono = new Hono()
  .get('/', (c) => c.text('Hello from Hono!'))
  .mount('/elysia', elysia.fetch)

const main = new Elysia()
  .get('/', () => 'Hello from Elysia')
  .mount('/hono', hono.fetch)
  .listen(3000)
```

## What interoperates

The page lists Hono, Nitro, H3, Next.js API routes, Nuxt API routes and SvelteKit API routes as frameworks that use Request/Response, and Bun, Deno, Vercel Edge Runtime, Cloudflare Worker and Netlify Edge Function as runtimes where this pattern can run.

## Gotchas

- Mount a function, not an app object: for Hono pass `hono.fetch`, for Elysia `elysia.fetch`.

## Checked

2026-11-07. Read in full: patterns/mount. Confirmed the WinterTC background, `.mount('/hono', hono.fetch)`, mounting Elysia inside Hono with `elysia.fetch` (when the other framework has `.mount`), and the framework and runtime lists. Removed a gotcha claiming Elysia lifecycle hooks, validation and context do not apply inside the mounted app; the page does not say that.

Method: documentation only; no commands were run.
