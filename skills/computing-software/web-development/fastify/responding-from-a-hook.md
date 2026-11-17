---
id: computing-software.web-development.fastify.responding-from-a-hook
name: responding-from-a-hook
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, async, reply, short-circuit]
level: advanced
status: docs-checked
description: "Send a response from a hook without mixing async and callback styles, which triggers FSTWRN003."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Warnings.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A hook can end the request by sending a reply, for example an auth failure in `onRequest`.

Replying from a hook stops the hook chain: the rest of the hooks and the handler are not executed. In an async hook, `reply.send()` must be called before the function returns or the promise resolves, otherwise the request proceeds. When `reply.send()` is called outside the promise chain, `return reply`, otherwise the request will be executed twice:

```js
fastify.addHook('onRequest', async (request, reply) => {
  if (!request.headers.authorization) {
    reply.code(401).send({ error: 'unauthorized' })
    return reply
  }
})
```

Callback hook: call `reply.send(...)` and return without calling `done()`; call `done()` only to continue the lifecycle:

```js
fastify.addHook('onRequest', (request, reply, done) => {
  if (!ok(request)) {
    reply.code(401).send({ error: 'unauthorized' })
    return
  }
  done()
})
```

If you want to respond with a stream, avoid using an `async` function for the hook:

```js
fastify.addHook('onRequest', (request, reply, done) => {
  reply.send(fs.createReadStream('some-file', 'utf8'))
})
```

Do not mix callbacks and `async`/Promise, otherwise the hook chain will be executed twice. In v5 plugins can no longer mix the callback and promise API, and warning FSTWRN003 ("The `%s` plugin mixes async and callback styles") reports it. The fix is to not mix the styles; `--disable-warning=FSTWRN003` can hide it but disabling warnings is not recommended.

Gotcha: in an async `preHandler` that sends via `setTimeout`/`setImmediate`, omitting `return reply` lets the hooks continue and fail with `FST_ERR_REP_ALREADY_SENT`.

## Checked

2026-11-04. Claims were checked against the official Fastify docs (Hooks.md, Warnings.md) read from the docs repository. Removed the unsourced Verify step.

Method: documentation only; no commands were run.
