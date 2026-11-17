---
id: computing-software.web-development.nuxt.nuxt-server-body-query-validated
name: nuxt-server-body-query-validated
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, server, read-body, get-query, validation]
level: practitioner
status: docs-checked
description: "Read request bodies and queries in Nuxt server handlers, with validated variants readValidatedBody and getValidatedQuery."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/2.directory-structure/1.server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Body: `const body = await readBody(event)` inside a handler named with a method suffix such as `submit.post.ts`. The page notes the suffix is there so the route matches POST requests that can carry a body; using `readBody` in a GET request throws a `405 Method Not Allowed` error. For runtime and type safety, use `readValidatedBody` with a schema validator such as Zod or Valibot.

Query: for `/api/query?foo=bar&baz=qux`, `getQuery(event)` gives access to `foo` and `baz`. For runtime and type safety use `getValidatedQuery` with a schema validator such as Zod or Valibot.

```ts
// server/api/query.get.ts
export default defineEventHandler((event) => {
  const query = getQuery(event)
  return { a: query.foo, b: query.baz }
})
```

Client side:

```ts
const { body } = await $fetch('/api/submit', { method: 'post', body: { test: 123 } })
```

## Checked

2026-11-08. Read in full from the nuxt/nuxt docs repository: docs/2.directory-structure/1.server.md (Body Handling and Query Parameters sections). Confirmed: readBody, the 405 note, getQuery, the validated variants and the $fetch call. Removed as unsupported by the page: the defineValidatedHandler claim (Standard Schema, typing the client call), the "usual source of malformed data" assertion, and the invented Verify step.

Method: documentation only; no commands were run.
