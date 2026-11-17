---
id: computing-software.web-development.hono.hono-dev-helper
name: hono-dev-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, debugging, routes]
level: intro
status: docs-checked
description: "List registered routes and identify the active router in Hono using the dev helper showRoutes and getRouterName."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/dev.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Dev helper

Import: `import { getRouterName, showRoutes } from 'hono/dev'`.

## getRouterName
```ts
const app = new Hono()
console.log(getRouterName(app))
```

## showRoutes
Prints registered routes to the console.

```ts
const app = new Hono().basePath('/v1')
app.get('/posts', (c) => { /* ... */ })
app.get('/posts/:id', (c) => { /* ... */ })
app.post('/posts', (c) => { /* ... */ })

showRoutes(app, { verbose: true })
```

Output:

```
GET   /v1/posts
        [handler]
GET   /v1/posts/:id
        [handler]
POST  /v1/posts
        [handler]
```

## Options
- `verbose: boolean`: show verbose information (handler lines).
- `colorize: boolean`: set `false` for uncoloured output (useful in CI logs).

## Gotcha
`showRoutes()` displays the registered routes in your console when the application starts running. `getRouterName(app)` returns the name of the router currently in use. Both are imported from `hono/dev`, described in the docs as useful methods for development. With `verbose: true` each route is followed by an indented `[handler]` line, and `basePath('/v1')` is included in the printed path. Set `colorize: false` for output without colors.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/dev.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe).

Method: documentation only; no commands were run.
