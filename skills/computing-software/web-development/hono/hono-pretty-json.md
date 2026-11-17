---
id: computing-software.web-development.hono.hono-pretty-json
name: hono-pretty-json
category: computing-software
field: web-development
product: hono
tags: [hono, middleware, json]
level: intro
status: docs-checked
description: "Pretty print JSON responses in Hono on demand with prettyJSON and its space, query and force options."
sources:
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/pretty-json.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pretty JSON

Import: `import { prettyJSON } from 'hono/pretty-json'`.

```ts
const app = new Hono()
app.use(prettyJSON()) // or prettyJSON({ space: 4 })
app.get('/', (c) => c.json({ message: 'Hono!' }))
```

`GET /` returns compact JSON; `GET /?pretty` returns indented JSON, e.g.

```
{
  "project": {
    "name": "Hono",
    "repository": "https://github.com/honojs/hono"
  }
}
```

## Options
- `space: number`: indentation, default `2`.
- `query: string`: query-string name that triggers it, default `pretty`.
- `force: boolean`: when `true`, always prettify regardless of the query. Default `false`.

## Gotcha
Adding `?pretty` to the URL query prettifies the JSON strings; without it `GET /` returns the compact form `{"project":{"name":"Hono","repository":"https://github.com/honojs/hono"}}`. `force: true` prettifies every JSON response regardless of the query parameter.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page middleware/builtin/pretty-json.md. Removed: the invented Verify step and the invented combined format example.
Method: documentation only; no commands were run.
