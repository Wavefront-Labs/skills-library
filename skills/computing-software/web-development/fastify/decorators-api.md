---
id: computing-software.web-development.fastify.decorators-api
name: decorators-api
category: computing-software
field: web-development
product: fastify
tags: [fastify, decorators, decorate-request, decorate-reply, encapsulation]
level: practitioner
status: docs-checked
description: "Extend the instance, request and reply with decorate, decorateRequest and decorateReply, and avoid the reference-type trap."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Decorators.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V5.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signatures: `fastify.decorate(name, value, [dependencies])` (server instance), `decorateRequest(name, value, [dependencies])`, `decorateReply(name, value, [dependencies])`. Check with `fastify.hasDecorator(name)`, `hasRequestDecorator`, `hasReplyDecorator`. `getDecorator(name)` works on the instance, request and reply; `request.setDecorator(name, value)` updates a Request decorator; both throw `FST_ERR_DEC_UNDECLARED` for an undeclared name (this catches typos). Decorating up front avoids the engine deoptimization caused by adding properties to the request after instantiation; initialize with `''` for strings and `null` for objects or functions.

```js
fastify.decorate('util', (a, b) => a + b)
fastify.decorateReply('html', function (payload) {
  this.type('text/html').send(payload)
})
fastify.decorateRequest('user', null)
fastify.addHook('onRequest', async (req) => { req.user = await load(req) })
```

An arrow function breaks the binding of `this` to the instance, request or reply; use `function` when you need it. On the server, `this` in route handlers is the decorated instance.

Reference types (objects, arrays) as the initial value for `decorateRequest`/`decorateReply` throw (`FST_ERR_DEC_REFERENCE_TYPE`): the object would be shared across all requests, and any mutation affects every request. Either declare the decorator without a value and assign a fresh object per request in an `onRequest` hook, or use the getter/setter pattern with a holder decorator:

```js
fastify.decorateRequest('my_decorator_holder')
fastify.decorateRequest('user', {
  getter () {
    this.my_decorator_holder ??= {}
    return this.my_decorator_holder
  }
})
```

Decorators also accept `{ getter, setter }` objects, e.g. `fastify.decorate('foo', { getter () { return 'a getter' } })` makes `fastify.foo` return `'a getter'`.

`dependencies` is an optional array of decorator names the new decorator relies on; an unsatisfied dependency throws, checked before the server boots. Defining the same name twice in the same encapsulated context throws; inside a child `register` the same name can be redefined without throwing.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Decorators.md, Plugins-Guide.md, Migration-Guide-V5.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
