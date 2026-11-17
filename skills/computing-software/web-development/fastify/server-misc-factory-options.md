---
id: computing-software.web-development.fastify.server-misc-factory-options
name: server-misc-factory-options
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, factory-options, ajv, plugin-timeout]
level: advanced
status: docs-checked
description: "Reference for less common factory options: pluginTimeout, exposeHeadRoutes, frameworkErrors, clientErrorHandler, ajv, serverFactory."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Options and defaults:

- `pluginTimeout`: 10000 ms, the maximum time a plugin can take to load; otherwise `ready` completes with an Error with code `ERR_AVVIO_PLUGIN_TIMEOUT`. `0` disables the check.
- `exposeHeadRoutes`: `true`. Each GET gets a sibling HEAD. To use a custom HEAD handler without disabling the option, define it before the GET route.
- `return503OnClosing`: `true`. After `close()`, requests get a 503 with `Connection: close`; when `false` they are processed normally but still get `Connection: close`.
- `allowErrorHandlerOverride`: `false`. When false, `setErrorHandler` cannot be called multiple times in the same scope.
- `frameworkErrors(error, req, res)`: default `null`; at present only `FST_ERR_BAD_URL` and `FST_ERR_ASYNC_CONSTRAINT` are implemented.
- `clientErrorHandler(err, socket)`: operates on the raw socket and must write a complete HTTP response (status line, headers, body), after checking that the socket is still writable. The default ignores `ECONNRESET` and otherwise answers 400.
- `ajv`: `{ customOptions, plugins, onCreate }` to configure the Ajv v8 instance without providing a custom one.
- `serializerOpts`: options for the default fast-json-stringify instance.
- `serverFactory(handler, opts)`: pass a custom HTTP server.
- `rewriteUrl(req)`: sync function receiving the raw request and returning a string; runs before routing.

```js
const fastify = require('fastify')({
  pluginTimeout: 30000,
  ajv: { customOptions: { allErrors: false }, plugins: [require('ajv-formats')] },
  frameworkErrors (error, req, res) {
    res.send(error.code === 'FST_ERR_BAD_URL' ? 'bad url' : error)
  }
})
```

Gotcha: `rewriteUrl` is not encapsulated; it is an instance-wide configuration. `frameworkErrors` receives `FST_ERR_BAD_URL` / `FST_ERR_ASYNC_CONSTRAINT` errors, so branch on the error and call `res.send(error)` for the rest.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Server.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
