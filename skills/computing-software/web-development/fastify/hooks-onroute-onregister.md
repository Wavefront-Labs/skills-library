---
id: computing-software.web-development.fastify.hooks-onroute-onregister
name: hooks-onroute-onregister
category: computing-software
field: web-development
product: fastify
tags: [fastify, hooks, on-route, on-register, plugins]
level: advanced
status: docs-checked
description: "Use onRoute to modify route options as routes are added, and onRegister to know when a plugin context is created."
sources:
  - https://github.com/fastify/fastify/blob/main/docs/Reference/Hooks.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Plugins-Guide.md
  - https://github.com/fastify/fastify/blob/main/docs/Guides/Migration-Guide-V4.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`onRoute(routeOptions)` is triggered when a new route is registered. The listener gets a `routeOptions` object as its sole parameter (`method`, `schema`, `url` including any prefix, `path` as a `url` alias, `routePath` without the prefix, `bodyLimit`, `logLevel`, `logSerializers`, `prefix`). The interface is synchronous, so listeners get no callback, and the hook is encapsulated. It is the place to modify options or add route hooks, for example:

```js
fastify.addHook('onRoute', (routeOptions) => {
  function onPreSerialization(request, reply, payload, done) {
    done(null, payload)
  }
  // preSerialization can be an array or undefined
  routeOptions.preSerialization = [...(routeOptions.preSerialization || []), onPreSerialization]
})
```

To add routes within an `onRoute` hook, tag them or the hook loops infinitely; the recommended approach uses the route `custom` option:

```js
const kRouteAlreadyProcessed = Symbol('route-already-processed')
fastify.addHook('onRoute', function (routeOptions) {
  const { url, method } = routeOptions
  const isAlreadyProcessed = (routeOptions.custom && routeOptions.custom[kRouteAlreadyProcessed]) || false
  if (!isAlreadyProcessed) {
    this.route({ url, method, custom: { [kRouteAlreadyProcessed]: true }, handler: () => {} })
  }
})
```

`onRegister(instance, opts)` is triggered when a new plugin is registered and a new encapsulation context is created; it runs before the registered code and is encapsulated. It is NOT called if the plugin is wrapped in `fastify-plugin`.

Since v4 route registration is synchronous (Migration Guide V4): an `onRoute` hook declared in a plugin should either have the routes wrapped in another plugin, or be followed by `await register(...)`. Since v3 both hooks are inherited within the encapsulation scope, so register them before registering plugins.

## Checked

2026-11-04. Every remaining claim, parameter name, default and example was read against the Fastify documentation sources (Hooks.md, Plugins-Guide.md, Migration-Guide-V4.md) and confirmed. Removed or corrected: the invented Verify step.

Method: documentation only; no commands were run.
