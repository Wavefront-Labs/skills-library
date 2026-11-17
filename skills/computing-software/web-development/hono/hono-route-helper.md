---
id: computing-software.web-development.hono.hono-route-helper
name: hono-route-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, routing, middleware, debugging]
level: practitioner
status: docs-checked
description: "Inspect matched routes in Hono with matchedRoutes, routePath, baseRoutePath and basePath, including index arguments and sub-app mounts."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/route.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Route helper

Import: `import { matchedRoutes, routePath, baseRoutePath, basePath } from 'hono/route'`.

```ts
app.get('/posts/:id', (c) => {
  const currentPath = routePath(c) // '/posts/:id'
  const routes = matchedRoutes(c)   // array of matched routes
  return c.json({ path: currentPath, totalRoutes: routes.length })
})
```

## With sub-apps
```ts
const apiApp = new Hono()
apiApp.get('/posts/:id', (c) =>
  c.json({
    routePath: routePath(c),       // '/api/posts/:id'
    baseRoutePath: baseRoutePath(c), // '/api'
    basePath: basePath(c),         // '/api' with actual params
  })
)
app.route('/api', apiApp)
```

## Functions
- `matchedRoutes(c)`: all routes matching the request, including middleware, e.g. `{ method: 'ALL', path: '/api/*', handler }` then `{ method: 'GET', path: '/api/users/:id', handler }`.
- `routePath(c)`: route pattern of the current handler. Optional index like `Array.prototype.at()`: `routePath(c, 0)` is `'/api/*'` (first matched), `routePath(c, -1)` is `'/api/users/:id'`.
- `baseRoutePath(c, index?)`: base path pattern as specified in routing, e.g. `'/:sub'` for `app.route('/:sub', subApp)`; with `app.route('/api', subApp)`, `baseRoutePath(c, 0)` is `'/'` and `baseRoutePath(c, -1)` is `'/api'`.
- `basePath(c)`: base path with real params embedded, e.g. `'/api'` for a request to `/api/posts/123` when mounted at `/:sub`.

## Gotcha
`routePath(c)` returns the route pattern (for example `/api/posts/:id`), while `basePath(c)` returns the base path with the real params embedded (for example `/api` when mounted at `/:sub` and requested as `/api/posts/123`). `baseRoutePath(c)` returns the base pattern as written in the routing (`/:sub`).

## Checked
2026-11-04: every claim left was read in the honojs/website docs page helpers/route.md. Removed: the invented Verify step.
Method: documentation only; no commands were run.
