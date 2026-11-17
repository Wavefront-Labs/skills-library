---
id: computing-software.web-development.nuxt.nuxt-server-errors-status-config
name: nuxt-server-errors-status-config
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, createerror, status-codes, runtime-config]
level: practitioner
status: docs-checked
description: "Return error codes with createError, custom success codes with setResponseStatus, and read runtimeConfig secrets and cookies in server handlers."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
If no errors are thrown, status is `200 OK`; any uncaught error returns a `500 Internal Server Error`. Throw `createError` for other codes:

```ts
export default defineEventHandler((event) => {
  const id = Number.parseInt(event.context.params.id) as number
  if (!Number.isInteger(id)) {
    throw createError({ status: 400, statusText: 'ID should be an integer' })
  }
  return 'All good'
})
```

For another success code, call `setResponseStatus(event, 202)` (the page's example returns 202 Accepted).

Runtime config on the server: declare `runtimeConfig: { githubToken: '' }` in `nuxt.config`, set `NUXT_GITHUB_TOKEN` in `.env`, then `const config = useRuntimeConfig()` and use `config.githubToken` in a handler (the page uses it in an Authorization header).

Cookies: `parseCookies(event)` returns the request cookies.

Redirects: `await sendRedirect(event, '/path/redirect/to', 302)`.

Streams (marked experimental, available in all environments): return `fs.createReadStream(...)` directly from the handler.

Legacy Node handlers can be wrapped with `fromNodeMiddleware((req, res) => ...)`, in routes or in `server/middleware`. The page advises avoiding legacy handlers as much as you can, and never combining the `next()` callback with a legacy middleware that is `async` or returns a Promise.

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (Error Handling, Status Codes, Runtime Config, Request Cookies, Sending Streams/Redirect, Legacy Handler sections). Confirmed: all code and behaviour above. Removed: the invented Verify (curl) step, the "private keys never reach the client" claim, and the unsourced "practical pattern" paragraph. Added the page's warning about next() with async legacy middleware.

Method: documentation only; no commands were run.
