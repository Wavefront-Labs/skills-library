---
id: computing-software.web-development.fastify.delay-accepting-requests
name: delay-accepting-requests
category: computing-software
field: web-development
product: fastify
tags: [fastify, plugins, hooks, readiness, http-503]
level: advanced
status: docs-checked
description: "Reject specific requests with 503 and Retry-After until an async prerequisite (like an OAuth key) is ready."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Delay-Accepting-Requests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: refuse requests that would fail as early as possible with useful context, while webhooks and health routes stay open.

Split into two plugins in one module:

```js
async function setup (fastify) {
  fastify.server.on('listening', doMagic)   // start after the server listens
  fastify.decorate('magicKey')              // placeholder
  function doMagic () {
    provider.thirdPartyMagicKeyGenerator(5000).catch((error) => {
      fastify.log.error({ error }, 'could not get key')
      fastify.close(() => process.exit(1))
    })
  }
}

const delay = (routes) =>
  function (fastify, opts, done) {
    fastify.addHook('onRequest', function (request, reply, next) {
      if (!request.server.magicKey) {
        reply.statusCode = 503
        reply.header('Retry-After', 5000)
        reply.send({ error: true, retryInMs: 5000 })
      }
      next()
    })
    fastify.register(routes, opts)
    done()
  }

module.exports = { setup: fp(setup), delay }
```

Use: `server.register(setup)`, keep `/ping` and `/webhook` outside, and `server.register(delay(customerRoutes), { prefix: '/v1' })`.

Why: do not wrap `delay` in fastify-plugin, so the hook stays in its scope; do wrap the inner routes plugin so they register in `delay`'s scope. A 503 tells load balancers to send traffic elsewhere.

Gotcha: catch errors in the async setup (an uncaught rejection crashes the app). State is per-instance, so it does not scale horizontally; store the key in a shared cache.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Delay-Accepting-Requests.md) and confirmed. Removed or corrected: advice to return after sending, which the guide does not give; the invented Verify step.

Method: documentation only; no commands were run.
