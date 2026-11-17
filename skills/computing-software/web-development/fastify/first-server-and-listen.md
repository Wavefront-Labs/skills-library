---
id: computing-software.web-development.fastify.first-server-and-listen
name: first-server-and-listen
category: computing-software
field: web-development
product: fastify
tags: [fastify, server, listen, getting-started]
level: intro
status: docs-checked
description: "Create a Fastify instance, declare a route and listen on the right host and port, including 0.0.0.0 for containers."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Getting-Started.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install with `npm i fastify`. Create the instance, declare a route and start it:

```js
const fastify = require('fastify')({ logger: true })

fastify.get('/', async (request, reply) => {
  return { hello: 'world' }
})

const start = async () => {
  try {
    await fastify.listen({ port: 3000 })
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()
```

With ESM add `"type": "module"` to package.json and use `import Fastify from 'fastify'`.

Listen defaults: `port` 0 (random), `host` localhost, and `exclusive`, `readableAll`, `writableAll`, `ipv6Only` all false. The Getting Started examples listen only on the loopback interface (127.0.0.1). To accept outside traffic, for example in Docker, pass `host: '0.0.0.0'` (all IPv4) or `host: '::'` (all IPv6 and, if the OS allows, IPv4). `::1` accepts only local IPv6.

```js
fastify.listen({ port: 3000, host: '0.0.0.0' }, function (err, address) {
  if (err) { fastify.log.error(err); process.exit(1) }
})
```

Plugin loading starts only when you call `listen()`, `inject()` or `ready()`.

Gotcha: with `0.0.0.0` the `address` passed to the callback is the first address the wildcard resolves to, not 0.0.0.0. The old variadic form `fastify.listen(8000)` was removed in v5; always pass an options object.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Getting-Started.md, Server.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
