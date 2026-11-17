---
id: computing-software.web-development.nuxt.nuxt-server-route-params-methods-catchall
name: nuxt-server-route-params-methods-catchall
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, route-params, http-methods, catch-all]
level: practitioner
status: docs-checked
description: "Server route filename conventions: [param], .get/.post suffixes, index.[method].ts namespaces and [...slug] catch-alls."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dynamic params use brackets in the filename: `server/api/hello/[name].ts` with `getRouterParam(event, 'name')` (params are also on `event.context.params`). For runtime and type safety use `getValidatedRouterParams` with a schema validator such as Zod or Valibot.

Method matching: suffix the file with `.get`, `.post`, `.put`, `.delete` and so on. With `test.get.ts` and `test.post.ts`, GET and POST return their own handler and any other method returns a 405 error. Inside a folder, `index.[method].ts` files are useful for API namespaces:

```
server/api/foo/index.get.ts   -> GET /api/foo
server/api/foo/index.post.ts  -> POST /api/foo
server/api/foo/bar.get.ts     -> GET /api/foo/bar
```

Catch-all: `server/api/foo/[...].ts` registers a catch-all for requests that match no other handler, such as `/api/foo/bar/baz`. `event.context.path` gives the route path (`/api/foo/bar/baz`) and `event.context.params._` gives the segment `bar/baz`. Name it with `[...slug].ts` to read `event.context.params.slug`.

Nested router: in `server/api/hello/[...slug].ts`, create an h3 `createRouter()`, add routes, and `export default useBase('/api/hello', router.handler)`.

The page notes server routes do not currently support the full dynamic-route functionality that pages do.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (Server Routes, Route Parameters, Matching HTTP Method, Catch-all Route, Nested Router sections). Confirmed: filename conventions, 405 behaviour, context fields. Removed: the cross-reference to a typed-fetch skill and the invented Verify step (curl checks).

Method: documentation only; no commands were run.
