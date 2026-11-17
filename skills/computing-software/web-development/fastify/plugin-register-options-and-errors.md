---
id: computing-software.web-development.fastify.plugin-register-options-and-errors
name: plugin-register-options-and-errors
category: computing-software
field: web-development
product: fastify
tags: [fastify, plugins, register, after, esm, errors]
level: practitioner
status: docs-checked
description: "Write plugins as async or callback functions, pass options (including functions), handle errors with after, and use ESM."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Plugins.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Write-Plugin.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Plugin signatures (pick one style, never both):

```js
module.exports = async function (fastify, options) {}
module.exports = function (fastify, options, done) { done() }
```

Register options: your own plugin options plus `prefix`, `logLevel`, `logSerializers`. These options are ignored for fastify-plugin wrapped plugins. The options can be a function evaluated at registration that receives the Fastify instance, so it sees decorators added by earlier plugins:

```js
fastify.register(fp(dbPlugin), { url: 'https://db.example' })
fastify.register(require('your-plugin'), parent => ({ connection: parent.db }))
```

Errors are handled by avvio: handle them in the next `after` or `ready` block, otherwise they are caught inside the `listen` callback:

```js
fastify.register(require('./database-connector')).after(err => {
  if (err) throw err
})
```

`after`, `ready` and `listen` support async/await, and `fastify` is thenable. `await fastify.register(...)` loads the plugin and its dependencies, finalizing encapsulation: later mutations to the plugin are not reflected in the parent.

ESM works: `export default async function plugin (fastify) {}` and `fastify.register(import('./plugin.mjs'))`.

Write-Plugin guide: a plugin must be tested (the guide uses node:test; a plugin without tests is not accepted to the ecosystem list), linted (the guide uses standard), and may use any license (MIT preferred). To avoid creating a new scope without fastify-plugin you can set `yourPlugin[Symbol.for('skip-override')] = true`, but it is not recommended.

Gotcha: the `fastify` instance passed to a plugin is encapsulated; decorators you add disappear unless wrapped in fastify-plugin.

A plugin that takes longer than `pluginTimeout` to load (default `10000` ms; `0` disables the check) makes `ready` complete with an error with code `ERR_AVVIO_PLUGIN_TIMEOUT` (Server.md).

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Plugins.md, Plugins-Guide.md, Write-Plugin.md, Server.md) and confirmed. Removed or corrected: the claim that only prefix is ignored for wrapped plugins (all three options are); the invented Verify step, replaced by the documented pluginTimeout behaviour.

Method: documentation only; no commands were run.
