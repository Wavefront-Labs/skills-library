---
id: computing-software.web-development.fastify.encapsulation-model
name: encapsulation-model
category: computing-software
field: web-development
product: fastify
tags: [fastify, encapsulation, plugins, scope, fastify-plugin]
level: practitioner
status: docs-checked
description: "How contexts inherit from parents, why siblings are isolated, and how fastify-plugin selectively breaks encapsulation."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Encapsulation.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every `register` call creates a child context. A child sees everything its ancestors added (decorators, hooks, schemas, parsers, error handlers) but never the reverse: parents and siblings do not see the child's additions.

```js
fastify.decorate('root', 1)
fastify.register(async (child) => {
  child.decorate('a', 2)           // visible in child and its descendants
  child.register(async (grand) => {
    console.log(grand.root, grand.a) // 1 2
  })
})
fastify.register(async (sibling) => {
  console.log(sibling.a)           // undefined
})
```

Wrap a plugin with `fastify-plugin` to make its decorators/hooks apply to the parent scope instead:

```js
const fp = require('fastify-plugin')
module.exports = fp(async function (fastify) { fastify.decorate('db', conn) })
```

This breaks encapsulation only for the wrapped plugin: non-fp registers nested inside it still create their own contexts. The same effect comes from setting `Symbol.for('skip-override')` on the function.

Docs example: with `fastify.decorateRequest('answer', 42)` at the root, an `authenticatedContext` (using @fastify/bearer-auth) sees `answer` only; a sibling `publicContext` that adds `foo` and its child `grandchildContext` that adds `bar` see `foo` but `/two` never sees `bar`, because `bar` lives in the grandchild. Wrapping `grandchildContext` in `fp(...)` makes `bar` visible to `publicContext` too (`/two` returns answer, foo and bar).

Everything in Fastify except the root context is a plugin, and each must still signal completion by returning a Promise (async) or calling `done`.

Gotcha: the Plugins guide says Fastify's encapsulation model lets you split an application into microservices later without refactoring; wrapping everything in fastify-plugin removes the isolation that gives you.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Encapsulation.md, Plugins-Guide.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
