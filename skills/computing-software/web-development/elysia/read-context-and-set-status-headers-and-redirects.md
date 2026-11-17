---
id: computing-software.web-development.elysia.read-context-and-set-status-headers-and-redirects
name: read-context-and-set-status-headers-and-redirects
category: computing-software
field: web-development
product: elysia
tags: [elysia, handler, context, status, headers, redirect, cookie]
level: practitioner
status: docs-checked
description: "Use the Elysia handler context: read body, query, params and headers, return status codes, set response headers, redirect, read cookies, request and IP."
sources:
  - https://elysiajs.com/essential/handler.html
  - https://elysiajs.com/tutorial/getting-started/status-and-headers/
  - https://elysiajs.com/tutorial/getting-started/handler-and-context/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: write a handler that reads request data and controls the response status, headers and redirect.

## Context

The handler's single argument is the context, unique per request except `store` (global mutable state). Properties: `body`, `query`, `params`, `headers`, `cookie`, `store`; utilities `redirect`, `status`, `set`; extras `request` (Web Standard Request), `server` (Bun server instance, only after `listen`), `path`.

```typescript
new Elysia().post('/', ({ body, query, headers }) => ({ body, query, headers }))
```

## status

Return `status(code, value)`; success defaults to 200.

```typescript
.get('/', ({ status }) => status(418, "I'm a teapot"))
```

The code can be a number or the string status name (`status("I'm a teapot", ...)`), which gives TypeScript autocompletion. The docs recommend returning status (never-throw) rather than throwing, because TypeScript can then check the value against the response schema, narrow by status code, and Eden can narrow errors. The legacy `set.status = 418` cannot infer the return type, but is useful in a plugin that sets a default status (201, 403...).

## Response headers

Use `set.headers`, not `headers` (which are the request headers):

```typescript
.get('/', ({ set }) => {
	set.headers['x-powered-by'] = 'Elysia'
	return 'a mimir'
})
```

Use lowercase names (`set-cookie`, not `Set-Cookie`).

## redirect

`return redirect('https://example.com')` or `redirect(url, 302)`. The returned value is ignored.

## Cookie, request, server

- `cookie: { name }` is a reactive proxy: read `name.value`, assign `name.value = 'x'`.
- `request.headers.get('user-agent')` for low-level access.
- Bun only: `server?.port`, and `server?.requestIP(request)` for the client IP.

## Gotchas

- Inline literal handlers (`.get('/', 'hi')`) are compiled ahead of time but are not a cache; lifecycle hooks can still change headers and status.
- The handler page says context can only be retrieved in a route handler.

## Checked

2026-11-07. Read in full: essential/handler, tutorial/getting-started/status-and-headers and tutorial/getting-started/handler-and-context. Confirmed the context property list, `status` (number or string name, never-throw advice, default 200), legacy `set.status`, `set.headers` with lowercase names, `redirect` (optional second argument 302, returned value ignored), the reactive cookie value, `request`, Bun-only `server` after `listen`, `server.requestIP(request)`, and that an inline value is not a cache. Replaced "Context is only available inside a handler (and hooks)" with the page's own wording; the "and hooks" part is not on these pages.

Method: documentation only; no commands were run.
