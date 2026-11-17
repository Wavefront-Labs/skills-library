---
id: computing-software.web-development.hono.hono-parse-body
name: hono-parse-body
category: computing-software
field: web-development
product: hono
tags: [hono, api, request, forms, file-upload]
level: practitioner
status: docs-checked
description: "Parse multipart and urlencoded bodies in Hono with c.req.parseBody, handling multiple files, repeated fields (all) and dot notation."
sources:
  - https://github.com/honojs/website/blob/main/docs/api/request.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Parsing form bodies

`await c.req.parseBody()` handles `multipart/form-data` and `application/x-www-form-urlencoded`.

```ts
app.post('/entry', async (c) => {
  const body = await c.req.parseBody()
  const data = body['foo'] // string | File
})
```

If several files share the same key, the LAST one wins.

## Multiple values
- Array suffix: `body['foo[]']` is always `(string | File)[]`. The `[]` postfix is required.
- Repeated names (`<input type="file" multiple />` or checkboxes with the same name): `await c.req.parseBody({ all: true })`. Then `body['foo']` is `(string | File)[]` if several, or `(string | File)` if one. `all` is off by default.

## Dot notation
```ts
const data = new FormData()
data.append('obj.key1', 'value1')
data.append('obj.key2', 'value2')

const body = await c.req.parseBody({ dot: true })
// { obj: { key1: 'value1', key2: 'value2' } }
```

## Related
`c.req.valid('form')` returns validated form data (see the Validation docs).

## Gotchas
- `all` is disabled by default; if several files share a key, the last one is used.
- Other body types use `json()`, `text()`, `arrayBuffer()`, `blob()` or `formData()`, not parseBody.

## Checked
2026-11-04: every claim left was read in the honojs/website docs page api/request.md. Removed: the invented Verify step, the bodyLimit, instanceof File and validator('form') advice, and the word silently.
Method: documentation only; no commands were run.
