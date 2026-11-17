---
id: computing-software.web-development.fastify.route-prefix-and-plugins
name: route-prefix-and-plugins
category: computing-software
field: web-development
product: fastify
tags: [fastify, routes, prefix, plugins, fastify-plugin]
level: practitioner
status: docs-checked
description: "Add a URL prefix to a group of routes with register options and avoid fastify-plugin dropping the prefix."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Routes.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pass `prefix` to `register`:

```js
fastify.register(require('./routes/v1/users'), { prefix: '/v1' })
// routes in the plugin: fastify.get('/users', h)  => GET /v1/users
```

Fastify handles the prefix at compilation time, so two plugins can both declare `/user` without conflict and performance is not affected. This works for nested `register`, and route parameters are supported in prefixes.

The `/` route inside a prefixed plugin: with a prefix `/something/`, a `/` route matches only `/something/`; with prefix `/something`, it matches both `/something` and `/something/`. The `prefixTrailingSlash` route option (`both` default, `slash`, `no-slash`) changes this.

`logLevel` and `logSerializers` can also be passed as register options and apply to the routes in that plugin. Plugin-level `logLevel` also affects `setNotFoundHandler` and `setErrorHandler`.

Gotcha: if `fastify-plugin` wraps the routes, the `prefix` option will not work. To make it work, wrap a plugin in a plugin:

```js
module.exports = fp(async function (app, opts) {
  app.register(routes, { prefix: '/v1' })
}, { name: 'my-routes' })
```

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Routes.md, Plugins.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
