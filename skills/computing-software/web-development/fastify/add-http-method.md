---
id: computing-software.web-development.fastify.add-http-method
name: add-http-method
category: computing-software
field: web-development
product: fastify
tags: [fastify, routes, http-methods, server]
level: advanced
status: docs-checked
description: "Add custom or previously removed HTTP methods with addHttpMethod and read the supported method list."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server.md lists the default methods as GET, HEAD, TRACE, DELETE, OPTIONS, PATCH, PUT, POST and QUERY; `addHttpMethod` adds non-standard methods that are supported by Node.js. The V5 Migration Guide says v5 removed PROPFIND, PROPPATCH, MKCOL, COPY, MOVE, LOCK, UNLOCK, TRACE and SEARCH, which can be added back with `addHttpMethod`.

```js
const fastify = Fastify()

// method without a body
fastify.addHttpMethod('REBIND')

// method that accepts a body
fastify.addHttpMethod('MKCOL', { hasBody: true })

// after adding, the route shorthand for the method works
fastify.mkcol('/', (req, reply) => {
  // Handle the 'MKCOL' request
})

console.log(fastify.supportedMethods) // string array
```

Options (both default `false`): `hasBody` (whether the method accepts a request body) and `overrideExisting` (explicitly override an existing method). Calling `addHttpMethod` for an existing method requires `overrideExisting: true` and overrides its body behavior, for example `fastify.addHttpMethod('GET', { hasBody: true, overrideExisting: true })`. Omitting it when the method already exists throws `FST_ERR_ROUTE_METHOD_ALREADY_SUPPORTED`.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Server.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
