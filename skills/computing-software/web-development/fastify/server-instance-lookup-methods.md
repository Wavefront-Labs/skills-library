---
id: computing-software.web-development.fastify.server-instance-lookup-methods
name: server-instance-lookup-methods
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, introspection, routes, plugins]
level: practitioner
status: docs-checked
description: "Inspect a running instance with addresses, listeningOrigin, hasRoute, findRoute, printRoutes, printPlugins and initialConfig."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Useful introspection APIs:

- `fastify.addresses()`: array of addresses the server listens on; empty before `listen()` or after `close()`.
- `fastify.listeningOrigin`: the current origin, such as `http://127.0.0.1:3000`, or the socket path for a Unix socket server.
- `fastify.hasRoute({ url, method, constraints })` returns true/false; `fastify.findRoute(...)` returns the route object or `null`. `url` and `method` are mandatory, `constraints` optional. In v5 `url` must be the route as defined (`'/example/:file(^\\d+).png'`), not a concrete URL.
- `fastify.printRoutes()`: route tree text; options include `commonPrefix: false`, `includeMeta` and `includeHooks`. The merged tree without a method is not the internal router structure, so do not use it for debugging.
- `fastify.printPlugins()`: the avvio plugin tree, useful for debugging require order issues.
- `fastify.prefix`, `fastify.pluginName`, `fastify.hasPlugin('name')` (relies on the plugin metadata name).
- `fastify.initialConfig`: frozen, read-only object of the initial options passed to the instance (only some properties are exposed).

```js
await fastify.ready()
console.log(fastify.printRoutes())
console.log(fastify.printRoutes({ commonPrefix: false, includeHooks: true }))
console.log(fastify.hasPlugin('my-plugin'))
```

`pluginName` (root plugin is `'fastify'`) resolves in this order: fastify-plugin metadata `name`; the `Symbol.for('fastify.display-name')` property; the filename if you `module.exports` the plugin; the function name of a regular function declaration.

`await using app = fastify()` works because the instance supports `Symbol.asyncDispose` (closed automatically when the scope ends).

Gotcha: call `printRoutes()` and `printPlugins()` inside or after a `ready` call. `hasRoute` with a concrete URL for a parametric route returns false in v5.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
