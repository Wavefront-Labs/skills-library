---
id: computing-software.web-development.hono.hono-method-override
name: hono-method-override
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, forms, method-override]
level: practitioner
status: docs-checked
description: "Let HTML forms trigger DELETE/PUT handlers in Hono with methodOverride using a form field, header or query parameter."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/method-override.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Method override

Import: `import { methodOverride } from 'hono/method-override'`.

It runs the handler of a different method than the actual request method, based on a form value, header or query, and returns its response. HTML forms can only send GET and POST, so put the real method in `_method`.

```html
<form action="/posts" method="POST">
  <input type="hidden" name="_method" value="DELETE" />
  <input type="text" name="id" />
</form>
```

```ts
const app = new Hono()
// With no options the form key `_method` is used.
app.use('/posts', methodOverride({ app }))

app.delete('/posts', () => {
  // ...
})
```

## Alternatives
```ts
app.use('/posts', methodOverride({ app, form: '_custom_name' }))
app.use('/posts', methodOverride({ app, header: 'X-METHOD-OVERRIDE' }))
app.use('/posts', methodOverride({ app, query: '_method' }))
```

## Options
- `app: Hono`: the Hono instance used in your application.
- `form: string`: form key, default `_method`.
- `header: string`: header name carrying the method.
- `query: string`: query parameter key carrying the method.

## Gotcha
With no options the form key `_method` is used; pass `header` or `query` to read the method from a header or query parameter instead.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page method-override.md. Removed: the invented Verify step, the claim that app is required, and the advice on registering the middleware before the handler.
Method: documentation only; no commands were run.
