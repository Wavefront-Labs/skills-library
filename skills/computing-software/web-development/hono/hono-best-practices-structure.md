---
id: computing-software.web-development.hono.hono-best-practices-structure
name: hono-best-practices-structure
category: computing-software
field: web-development
product: hono
tags: [hono, guide, best-practices, structure, typescript]
level: practitioner
status: docs-checked
description: "Structure a larger Hono app without Rails-style controllers: inline handlers, factory.createHandlers and app.route splitting, with RPC chaining."
sources:
  - https://github.com/honojs/website/blob/main/docs/guides/best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Best practices: structuring a Hono app

## Avoid Rails-like controllers
Extracting a handler into `const booksList = (c: Context) => ...` loses path-param inference (`c.req.param('id')` cannot be inferred without complex generics). Write handlers directly after the path:

```ts
app.get('/books/:id', (c) => {
  const id = c.req.param('id') // inferred
  return c.json(`get ${id}`)
})
```

If you still want separate handlers, use `factory.createHandlers()` from `hono/factory`; inference then works:

```ts
const factory = createFactory()
const middleware = factory.createMiddleware(async (c, next) => { c.set('foo', 'bar'); await next() })
const handlers = factory.createHandlers(logger(), middleware, (c) => c.json(c.var.foo))
app.get('/api', ...handlers)
```

## Larger apps with app.route()
```ts
// authors.ts
const app = new Hono()
app.get('/', (c) => c.json('list authors'))
app.post('/', (c) => c.json('create an author', 201))
app.get('/:id', (c) => c.json(`get ${c.req.param('id')}`))
export default app

// index.ts
const app = new Hono()
app.route('/authors', authors)
app.route('/books', books)
export default app
```

## For RPC, chain
Chain the methods so types accumulate, then export the type:

```ts
const app = new Hono()
  .get('/', (c) => c.json('list authors'))
  .post('/', (c) => c.json('create an author', 201))
  .get('/:id', (c) => c.json(`get ${c.req.param('id')}`))
export default app
export type AppType = typeof app
```
`hc<AppType>('http://localhost')` is then typed correctly.

## Gotcha
Controller-style handlers typed with `Context` cannot infer path params. For RPC, the page says to chain the methods to get the correct type.

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/guides/best-practices.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the overstated "silently degrades" and "invisible to RPC" claims.

Method: documentation only; no commands were run.
