---
id: computing-software.web-development.fastify.route-url-patterns
name: route-url-patterns
category: computing-software
field: web-development
product: fastify
tags: [fastify, routes, params, wildcards, regex]
level: practitioner
status: docs-checked
description: "Define route paths with params, wildcards, regex, multiple params, optional params and escaped colons."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Static routes are always checked before parametric and wildcard routes. Patterns:

```js
fastify.get('/example/:userId', h)               // parametric
fastify.get('/example/*', h)                      // wildcard
fastify.get('/example/:file(^\\d+).png', h)       // regex param
fastify.get('/plugins/:name-:version', h)         // multiple in a segment
fastify.get('/near/:lat-:lng/radius/:r', h)       // several params, use "-" as separator
fastify.get('/at/:hour(^\\d{2})h:minute(^\\d{2})m', h) // several regex params
fastify.get('/posts/:id?', h)                     // optional (last) param
fastify.post('/name::verb', h)                    // literal colon: /name:verb
```

Params end up in `request.params`. In v5 that object has no prototype: use `Object.hasOwn(request.params, 'id')`, not `request.params.hasOwnProperty`. An optional param is `undefined` when absent.

Implicitly optional parameters stopped working in v4: you get a 404 unless you declare them explicitly with `?`.

Security: route params and wildcards are percent-decoded before reaching the handler (`/download/..%2fsecret.txt` gives `request.params.file === '../secret.txt'`). Parameters are untrusted input; do not pass them to `path.join`, `fs` APIs, template engines or redirects without validation or containment. To serve a directory use `@fastify/static`.

Performance: RegExp routes are expensive, and multiple parameters can hurt performance on hot paths; prefer static or single-parameter routes.

Gotcha: `maxParamLength` (default 100) caps parametric route param length; when exceeded, the not found route is invoked.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Routes.md, Migration-Guide-V4.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
