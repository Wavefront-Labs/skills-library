---
id: computing-software.web-development.trpc.runtime-configuration-options
name: runtime-configuration-options
category: computing-software
field: web-development
product: trpc
tags: [trpc, inittrpc, isserver, isdev, allowoutsideofserver]
level: practitioner
status: docs-checked
description: "The initTRPC.create options: transformer, errorFormatter, isDev, isServer, allowOutsideOfServer, with their defaults."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/routers.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`initTRPC.create(config)` accepts a runtime configuration object. From the v11 docs:

- `transformer`: use a data transformer; see the data transformer skill.
- `errorFormatter`: custom shaping of the error returned to clients.
- `allowOutsideOfServer` (default `false`): lets `@trpc/server` run in non-server environments. The docs flag this as use-with-caution, mainly for testing.
- `isServer` (default `typeof window === 'undefined' || 'Deno' in window || process.env.NODE_ENV === 'test'`): whether this is a server environment. Also use with caution.
- `isDev` (default `process.env.NODE_ENV !== 'production'`): decides whether the API returns stack traces in error responses.

```ts
import { initTRPC } from '@trpc/server';
const t = initTRPC.create({ isDev: false });
```

The error-handling page notes that stack traces are only included in `error.data.stack` when `isDev` is true, and advises overriding `isDev` manually if you need deterministic behaviour across runtimes.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/routers.md (read in full): the Runtime Configuration `RootConfig` block with its defaults and the "use with caution" warnings; www/v11/docs/server/error-handling.md (read in full): "Stack traces in production" (error.data.stack only when isDev is true, default NODE_ENV check, override for deterministic behaviour across runtimes).

Removed or corrected: the edge-runtime example, the "typical use" paragraph about jsdom tests (not on either page), the "for example superjson" detail on `transformer` (routers.md does not name it), "when to override them" from the description, and the invented Verify step.

Method: documentation only; no commands were run.
