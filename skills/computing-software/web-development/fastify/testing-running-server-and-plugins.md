---
id: computing-software.web-development.fastify.testing-running-server-and-plugins
name: testing-running-server-and-plugins
category: computing-software
field: web-development
product: fastify
tags: [fastify, testing, listen, supertest, plugins]
level: practitioner
status: docs-checked
description: "Test with a real listening server using fetch, undici or SuperTest, and unit-test plugins with decorators."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Real server with `fetch` (Node 18+):

```js
test('should work with fetch', async t => {
  const fastify = buildFastify()
  t.after(() => fastify.close())
  await fastify.listen()    // random port
  const response = await fetch('http://localhost:' + fastify.server.address().port)
  t.assert.strictEqual(response.status, 200)
})
```

With undici use `new Client('http://localhost:' + port, { keepAliveTimeout: 10, keepAliveMaxTimeout: 10 })` and close both client and server in `t.after`.

SuperTest without listening:

```js
await fastify.ready()
const response = await supertest(fastify.server).get('/').expect(200)
```

Testing a plugin: register it on a fresh instance, add a route that reads what the plugin decorated, and inject.

```js
const myPlugin = fP(async function (fastify) {
  fastify.decorateRequest('helloRequest', 'Hello World')
  fastify.decorate('helloInstance', 'Hello Fastify Instance')
})

test('plugin', async t => {
  const fastify = Fastify()
  fastify.register(myPlugin)
  fastify.get('/', async (request) => ({ message: request.helloRequest }))
  const res = await fastify.inject({ method: 'GET', url: '/' })
  t.assert.deepStrictEqual(JSON.parse(res.body), { message: 'Hello World' })
})
```

Gotcha: without `fastify-plugin` the decorators stay in the plugin's context and the route sees nothing. `listen()` without close keeps the process alive.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Testing.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
