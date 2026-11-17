---
id: computing-software.web-development.nextjs.middleware-edge-runtime-and-deployment
name: middleware-edge-runtime-and-deployment
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, middleware, edge-runtime, vercel, self-hosted, docker, deployment, cold-start, node-runtime, web-development]
level: advanced
status: gated
description: "Next.js middleware and the edge runtime's real constraints (no Node APIs, size limits), and deployment gotchas self-hosting outside Vercel."
sources:
  - https://nextjs.org/docs/app/building-your-application/routing/middleware
  - https://nextjs.org/docs/app/api-reference/edge
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Next.js middleware, the edge runtime, and deploying off Vercel

**Goal:** know what the edge runtime can't do before writing middleware that
works locally and breaks only in production, and know what self-hosting gives up
compared to Vercel's managed platform.

## 1. Middleware runs on every matched request, before rendering
In Next 16 the file is `proxy.ts` exporting `proxy` (ran on 16.4.2: `middleware.ts` still works but the build prints `The "middleware" file convention is deprecated. Please use "proxy" instead`, and the route table lists `Proxy (Middleware)`). The text below says "middleware" for both. It runs before a request reaches a route —
use it for auth gating, A/B routing (rewrite based on a cookie), locale
redirects, or header injection. It does **not** run inside page rendering, so it
can't read a Server Component's data or affect what that component fetches —
only the request/response (headers, cookies, redirect, rewrite) in transit.
Use `matcher` in the exported `config` to scope which paths run through it —
without scoping, it runs on every single request including static assets, which
is pure overhead for routes that don't need it.

## 2. Edge runtime constraints — the ones that bite in production
A `middleware.ts` file runs on the **Edge Runtime** by default, a restricted V8-isolate
environment, not full Node (ran: importing `node:fs` in `middleware.ts` printed `A Node.js module is loaded ('node:fs') which is not supported in the Edge Runtime` at build time while the build still exited 0, so treat that warning as a runtime failure). A `proxy.ts` file defaults to the **Node.js** runtime (ran: `fs.existsSync` worked in `proxy.ts`), and the proxy docs say the `runtime` config option is not available there. A `middleware.ts` with `export const runtime = 'nodejs'` also built and ran with `fs` on 16.4.2. The constraints below apply to the Edge Runtime:
- No Node built-ins that need OS bindings: no `fs`, no raw TCP (`net`), no
  native modules. A library that transitively imports `fs` (many "universal"
  npm packages do, even unused code paths) fails to build or throws at runtime
  on the edge even though it imports fine locally under Node for a page.
- Do not rely on in-memory state in middleware surviving between requests: isolates on a hosted edge platform can be created and recycled independently (gated: unconfirmed, source is paywalled or blocked). This is platform behaviour that cannot be reproduced locally.
- A code size limit that varies by host (check your platform's current
  limit) - a middleware file that imports a large library (a big validation
  schema set, an ORM client) can exceed it where the same import is fine in a
  Node-runtime route.
- `crypto`/`fetch`/standard Web APIs are available; database drivers requiring a
  raw TCP socket (most traditional Postgres/MySQL clients) are not - use an
  HTTP-based driver if you need DB access from the Edge Runtime, use `proxy.ts`
  (Node runtime), or move that logic to a Node-runtime route handler and have
  middleware just rewrite to it. Raw-TCP driver support on hosted edge platforms is unconfirmed here (gated: unconfirmed, source is paywalled or blocked); it could not be tested locally.
- Route handlers and pages run on Node by default; set `export const runtime = 'edge'`/`'nodejs'` on a route only when you need a specific one.

## 3. Self-hosting vs Vercel — what you take on
Running `next start` (or `output: 'standalone'` in Docker) works, but you now own
things Vercel's platform otherwise provides:
- **Cache across instances**: the default cache is in-memory and not shared across
  instances; for consistent ISR/`use cache` behaviour behind several instances use a
  shared cache handler (`cacheHandler` for ISR, `cacheHandlers`/`'use cache: remote'`
  for `use cache`), per the self-hosting guide.
- **Image Optimization**: works with zero configuration under `next start` (it uses
  `sharp`; on glibc Linux the guide mentions extra memory-allocator configuration).
  You can set `unoptimized` or a custom loader if you prefer a separate service.
- **Edge network**: self-hosted middleware runs wherever your Node process runs
  — one region, not globally distributed — so edge-specific latency wins don't
  apply the same way.
- Build output: use `output: 'standalone'` for Docker to get a minimal
  `node_modules` tree copied automatically; forgetting this ships either a
  broken image missing deps or an unnecessarily huge one.

## Verify
- [ ] `middleware.ts` has a scoped `matcher` — it isn't running on every static asset by default.
- [ ] Any library imported into middleware is confirmed edge-compatible (no transitive `fs`/`net` usage) before it ships.
- [ ] DB access from middleware/edge routes uses an HTTP-based driver, not a raw TCP client.
- [ ] Self-hosted ISR uses a shared revalidation cache if running more than one instance.
- [ ] `next/image` optimization is either served by a running loader or explicitly disabled (`unoptimized`) in self-hosted deployments.
