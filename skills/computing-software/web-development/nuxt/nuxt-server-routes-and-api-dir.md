---
id: computing-software.web-development.nuxt.nuxt-server-routes-and-api-dir
name: nuxt-server-routes-and-api-dir
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, api-routes, define-event-handler, nitro]
level: intro
status: docs-checked
description: "Create API and server routes under server/api and server/routes with defineEventHandler, and keep Vue app code out of the Nitro bundle."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nuxt scans `server/api`, `server/routes` and `server/middleware` and registers handlers with HMR. Each file default-exports a function defined with `defineEventHandler()` (alias `eventHandler()`); the handler can return JSON data, a Promise or a `Response` object.

```ts
// server/api/hello.ts
export default defineEventHandler((event) => {
  return { hello: 'world' }
})
```

Call it universally from pages and components: `const { data } = await useFetch('/api/hello')`.

- Files in `server/api` are prefixed with `/api`.
- Files in `server/routes` are not: `server/routes/hello.ts` is served at `/hello`.
- `nuxt/server` is the import surface for server utilities and what the server auto-imports resolve to; it is not tied to a particular h3 or Nitro version.
- Server routes do not currently support the full dynamic-route functionality that pages do.

Important (stated on the page): do not import Vue app code (components, composables or other app-only utilities) in server routes or utilities, and do not import server-only code in your app. The page links to a "Why you cannot mix Vue and Nitro code" section in the shared-directory docs.

Server routes are powered by h3, which comes with a set of helpers.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (intro and Server Routes sections). Confirmed: directories, prefixes, handler return types, nuxt/server note and the import boundary. Removed: the unsupported explanation of two bundles breaking builds or leaking code, the advice to share code via shared/ (the page only links to that explanation), the list of specific helper names, and the invented Verify (curl) step.

Method: documentation only; no commands were run.
