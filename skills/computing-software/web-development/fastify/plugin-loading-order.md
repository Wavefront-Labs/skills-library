---
id: computing-software.web-development.fastify.plugin-loading-order
name: plugin-loading-order
category: computing-software
field: web-development
product: fastify
tags: [fastify, plugins, register, architecture, getting-started]
level: intro
status: docs-checked
description: "Structure an app as plugins loaded in a predictable order, with a database connector wrapped in fastify-plugin."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
In Fastify everything is a plugin and `register` is the only way to add routes, plugins and utilities. Fastify loads plugins in declaration order and starts the next only after the current one finished (via avvio), so a DB connector registered first is usable by later plugins.

Recommended order, repeated inside each sub-service when you want a subset of routes to have its own setup:

```
plugins (from the Fastify ecosystem)
your plugins (custom)
decorators
hooks
your services
```

Database connector wrapped so its decorators reach the parent scope:

```js
const fastifyPlugin = require('fastify-plugin')

async function dbConnector (fastify, options) {
  fastify.register(require('@fastify/mongodb'), {
    url: 'mongodb://localhost:27017/test_database'
  })
}
module.exports = fastifyPlugin(dbConnector)
```

Then `fastify.register(require('./our-db-connector'))` followed by `fastify.register(require('./our-first-routes'))`; the routes plugin can use `fastify.mongo.db`.

Plugin signature: `function (fastify, options, done)` or `async function (fastify, options)`. Never mix the two styles: in v5 plugins can no longer mix the callback and promise API, so an `async` plugin must not also take or call `done`.

Wrapping a plugin function with `fastify-plugin` exposes the decorators and hooks declared inside it to the parent scope; without it they stay encapsulated. Plugin loading starts when you call `fastify.listen()`, `fastify.inject()` or `fastify.ready()`.

If you want only a subset of routes to have its own setup, replicate the same structure inside a service (service A, service B), each with its own plugins, decorators, hooks and services.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Getting-Started.md, Plugins-Guide.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
