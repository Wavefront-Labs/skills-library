---
id: computing-software.web-development.fastify.testing-with-inject
name: testing-with-inject
category: computing-software
field: web-development
product: fastify
tags: [fastify, testing, inject, light-my-request, node-test]
level: practitioner
status: docs-checked
description: "Test routes without a network using fastify.inject and node:test, with app and server code split."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Separate app construction from listening so tests can build the app:

```js
// app.js
const fastify = require('fastify')
function build (opts = {}) {
  const app = fastify(opts)
  app.get('/', async () => ({ hello: 'world' }))
  return app
}
module.exports = build
```

```js
// app.test.js
const { test } = require('node:test')
const build = require('./app')

test('requests the "/" route', async t => {
  t.plan(1)
  const app = build()
  t.after(() => app.close())
  const response = await app.inject({ method: 'GET', url: '/' })
  t.assert.strictEqual(response.statusCode, 200, 'returns a status code of 200')
})
```

`inject` (powered by `light-my-request`) waits for plugins to boot, then fakes the HTTP request. Options: `method`, `url`, `query`, `payload`, `headers`, `cookies`. It also supports callbacks, promises and a chain form:

```js
fastify.inject().get('/').headers({ foo: 'bar' }).query({ foo: 'bar' }).end((err, res) => {})
```

Response helpers: `response.statusCode`, `response.headers`, `response.body`, `response.payload`, `response.json()`.

Set `"test": "node --test"` (add `--watch` while developing). Debug with `node --test --test-only --inspect-brk test/file.test.js` and `{ only: true }` on a test.

Gotcha: always call `.close()` at the end so connections to external services are closed. Passing `logger` options only in `server.js` keeps test output quiet.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Testing.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
