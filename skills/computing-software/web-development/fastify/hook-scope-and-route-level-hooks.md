---
id: computing-software.web-development.fastify.hook-scope-and-route-level-hooks
name: hook-scope-and-route-level-hooks
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, encapsulation, routes, scope]
level: advanced
status: docs-checked
description: "Scope hooks to a plugin or a single route, and understand ordering and the this binding."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Except for `onClose`, all hooks are encapsulated: a hook added inside `register` applies only to that context and its children, and a function hook is bound to the right Fastify context as `this`. To limit a hook to a subset of routes, put them in a plugin:

```js
fastify.register((instance, opts, done) => {
  instance.addHook('preHandler', (request, reply, done) => {
    request.timestamp = new Date(); done()
  })
  instance.get('/plugin1', (request, reply) => reply.send(request))
  done()
})
fastify.get('/plugin2', (request, reply) => reply.send({}))
```

Only `/plugin1` gets the hook.

Route-level hooks (`onRequest`, `onResponse`, `preParsing`, `preValidation`, `preHandler`, `preSerialization`, `onSend`, `onTimeout`, `onError`) are unique to the route and always run last in their category, after the shared hooks. Multiple can be given as an array:

```js
fastify.route({
  method: 'GET',
  url: '/',
  preHandler: [function (request, reply, done) { done() }],
  handler: function (request, reply) { reply.send({ hello: 'world' }) }
})
```

Notes:
- Arrow functions do not receive `this` as the Fastify instance; it is the `this` of the current scope.
- Custom properties set on the request in hooks need TypeScript declaration merging: `declare module 'fastify' { export interface FastifyRequest { authenticatedUser?: AuthenticatedUser } }`. Use a new property name so you do not mutate existing ones.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md, Plugins-Guide.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
