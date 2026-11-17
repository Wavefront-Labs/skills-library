---
id: computing-software.web-development.hono.hono-routing-grouping
name: hono-routing-grouping
category: computing-software
field: web-development
product: hono
tags: [hono, api, routing, basepath, sub-apps]
level: practitioner
status: docs-checked
description: "Organize Hono routes with app.route, basePath, grouping without a base, and avoid the ordering bug that causes silent 404s."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grouping and base paths

## route()
```ts
const book = new Hono()
book.get('/', (c) => c.text('List Books'))          // GET /book
book.get('/:id', (c) => c.text('Get Book: ' + c.req.param('id'))) // GET /book/:id
book.post('/', (c) => c.text('Create Book'))        // POST /book

const app = new Hono()
app.route('/book', book)
```

## Keep the base
```ts
const book = new Hono()
book.get('/book', ...)  // GET /book
const user = new Hono().basePath('/user')
user.get('/', ...)      // GET /user

const app = new Hono()
app.route('/', book)
app.route('/', user)
```

## basePath
`const api = new Hono().basePath('/api'); api.get('/book', ...)` serves `GET /api/book`.

## Grouping order gotcha
`route()` takes the stored routing from the second argument and adds it to its own, so register routes on a sub-app BEFORE it is grouped; the wrong order returns 404. Correct order:

```ts
three.get('/hi', (c) => c.text('hi'))
two.route('/three', three)
app.route('/two', two)       // GET /two/three/hi -> 200
```

Wrong order gives 404, because `two` had no routes when it was mounted:

```ts
three.get('/hi', (c) => c.text('hi'))
app.route('/two', two)       // two has no routes yet
two.route('/three', three)   // GET /two/three/hi -> 404
```

Build from the innermost sub-app outward.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/routing.md. Removed: the invented Verify step and the Notes on notFound and onError priority, which are not on the cited page.
Method: documentation only; no commands were run.
