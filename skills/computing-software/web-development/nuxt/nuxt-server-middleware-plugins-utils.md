---
id: computing-software.web-development.nuxt.nuxt-server-middleware-plugins-utils
name: nuxt-server-middleware-plugins-utils
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, middleware, nitro-plugin, server-utils]
level: practitioner
status: docs-checked
description: "Use server/middleware, server/plugins and server/utils, plus the #server alias and server/types, in a Nuxt project."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server middleware: any file in `server/middleware` runs on every request before any other server route, to add or check headers, log requests or extend the request object. It should not return anything (nor close or respond to the request); it only inspects or extends the request context, or throws.

```ts
// server/middleware/auth.ts
export default defineEventHandler((event) => {
  event.context.auth = { user: 123 }
})
```

Server plugins: files in `server/plugins` register as Nitro plugins, to extend Nitro's runtime behaviour and hook lifecycle events: `export default definePlugin((nitroApp) => {...})` (the page imports `definePlugin` from `nitro`).

Server utilities: server routes are powered by h3 and its helpers; add your own in `server/utils`. Only files directly in `server/utils` are auto-imported; to auto-import from a subdirectory, re-export from a top-level file. The page's example is a `defineWrappedResponseHandler` that wraps a handler with try/catch and returns `{ response }` or `{ err }`.

Alias (v4.3): `#server` imports from anywhere within `server/` regardless of the importing file's location (`import { formatUser } from '#server/utils/formatUser'`). It can only be used within `server/`; importing it in client code errors.

Types: `server/` runs in a different context from `app/`, so auto-imports and types differ. Nuxt 4 generates a `tsconfig.json` with a project reference covering `server/`. Types in `server/types/` are auto-imported in the server context only, top-level files only (nested subdirectories are not scanned). Types also needed in the Vue app belong in `shared/types/`.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (Server Middleware, Plugins, Utilities, Alias, Types sections). Confirmed: all items above. Removed: the invented Verify step (including the claim about assets handled by Nitro).

Method: documentation only; no commands were run.
