---
id: computing-software.web-development.nextjs.server-only-code-and-env-exposure
name: server-only-code-and-env-exposure
category: computing-software
field: web-development
product: nextjs
tags: [nextjs, server-only, client-only, next-public-env, environment-variables, secrets, taint, web-development]
level: practitioner
status: verified
description: "Keeping secrets and server code out of Next.js client bundles: server-only/client-only packages, NEXT_PUBLIC_ inlining rules, runtime env and taint APIs."
sources:
  - https://nextjs.org/docs/app/getting-started/server-and-client-components#preventing-environment-poisoning
  - https://nextjs.org/docs/app/guides/environment-variables
  - https://react.dev/reference/react/experimental_taintObjectReference
  - https://www.npmjs.com/package/server-only
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# server-only, client-only and env var exposure

**Goal:** a build-time guarantee that DB clients, API keys and internal modules never reach the browser.

## 1. server-only
```ts
// lib/db.ts
import "server-only";
export const db = new PrismaClient();
```
Importing this module from any client component fails the **build** (ran on 16.4.2 with a Turbopack build: `Error: You're importing a module that depends on "server-only"...`, with an import trace through the client component; the wording mentions the Pages Router for the client-browser graph, so read the import trace). The `server-only` package itself just throws on import. Put it in every module that touches secrets, the DB, or internal services. The `client-only` marker package (npm: `This is a marker package to indicate that a module can only be used in Client Components`) is the reverse for browser-only modules.

## 2. Env var rules
- `process.env.SECRET` without prefix: available on the server only; in client code it's `undefined`.
- `NEXT_PUBLIC_*`: **inlined into the JS bundle at build time** as literals. Public forever once shipped; changing it requires a rebuild. Never prefix secrets.
- Dynamic lookups: the env docs say `process.env[name]` is not inlined. Ran on a 16.4.2 Turbopack production build: a client `useEffect` reading `process.env[name]` returned the `NEXT_PUBLIC_` value, and a non-public name returned `undefined`, so the behaviour is not a guarantee; always use the literal `process.env.NEXT_PUBLIC_X` form in client code. An unprefixed variable read in a Client Component is `undefined` in the browser (ran), but a Client Component is also rendered on the server for the initial HTML, where the real value is visible, so never read secrets there.
- Load order (env docs, and ran with `.env`, `.env.local`, `.env.production`): `process.env` > `.env.$(NODE_ENV).local` > `.env.local` (not checked when `NODE_ENV` is `test`) > `.env.$(NODE_ENV)` > `.env`. Ran: a process variable beat `.env.local`, which beat `.env.production`, which beat `.env`. Commit `.env.example`, never `.env.local`.

## 3. Runtime config for one image, many environments
Because `NEXT_PUBLIC_` is build-time, a single Docker image can't switch public values per environment. Options: read server env in a server component and pass it as a prop, or serve a `/config` endpoint. Server-side `process.env` is read at runtime for dynamic routes (static routes capture values at build).

## 4. Validate env at startup
```ts
// env.ts
import "server-only";
import { z } from "zod";
export const env = z.object({ DATABASE_URL: z.string().url(), STRIPE_SECRET: z.string().min(1) }).parse(process.env);
```
The `@t3-oss/env-nextjs` package (exists on npm) offers a client/server split; read its docs for behaviour.

## 5. Taint (defence in depth)
```ts
import { experimental_taintObjectReference, experimental_taintUniqueValue } from "react";
experimental_taintUniqueValue("Do not pass the API key to the client", process, process.env.API_KEY!);
```
Requires `experimental.taint: true` (taint config docs: experimental; enabling it also taints `process.env` so it cannot be passed whole to a Client Component and switches the app directory to React's experimental channel). Prevents accidentally passing tainted objects/values as client props. Not a substitute for DTOs.

## 6. Other leak paths
- Server actions return values to the client - return only what the UI needs.
- Props to client components are visible in the RSC payload (view-source shows them).
- Source maps in production expose server code paths if `productionBrowserSourceMaps` is on.

## Verify
- [ ] `grep -r "NEXT_PUBLIC_" .env*` - none of these are secrets.
- [ ] Search built client chunks for a known secret prefix: `grep -r "sk_live" .next/static` returns nothing.
- [ ] Every DB/secret module imports `server-only`.
