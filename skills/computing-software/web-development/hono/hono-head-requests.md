---
id: computing-software.web-development.hono.hono-head-requests
name: hono-head-requests
category: computing-software
field: web-development
product: hono
tags: [hono, guide, http, head-requests]
level: practitioner
status: docs-checked
description: "Handle HEAD requests correctly in Hono: they are converted to GET before routing, so dedicated app.head handlers never run; use middleware for HEAD logic."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# HEAD requests in Hono

Hono automatically converts HEAD requests to GET and strips the response body. This happens in the dispatch layer BEFORE route matching.

## Do: write GET routes
```ts
app.get('/api/users', async (c) => {
  const users = await getUsers()
  c.header('X-Total-Count', users.length.toString())
  return c.json(users)
})
// HEAD /api/users: same headers (incl. X-Total-Count), status 200, null body
```

## Do: middleware for HEAD-specific logic
```ts
app.use('/api/resource', async (c, next) => {
  await next()
  if (c.req.method === 'HEAD') {
    c.header('X-HEAD-Processed', 'true')
    c.res = new Response(null, c.res) // skip body content
  }
})
```

## Don't: dedicated HEAD handlers
```ts
app.head('/api/users', (c) => { /* NEVER called */ })
app.on('HEAD', '/api/users', (c) => { /* still converted to GET */ })
```

## Performance and middleware
Avoid expensive body generation in GET handlers if you expect many HEAD requests (detect HEAD in middleware). Cache headers behave identically. Body-processing middleware such as compression automatically skips HEAD.

## Test both
```ts
const getRes = await app.request('/api/users')
const headRes = await app.request('/api/users', { method: 'HEAD' })
expect(headRes.status).toBe(getRes.status)
expect(headRes.headers.get('X-Total-Count')).toBe(getRes.headers.get('X-Total-Count'))
expect(headRes.body).toBe(null)
```

## Gotcha
`app.head()` and `app.on('HEAD', ...)` look valid but are dead code. For completely different HEAD logic, use a different endpoint.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/guides/best-practices.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
