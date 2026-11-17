---
id: computing-software.web-development.elysia.build-configurable-deduplicated-and-lazy-plugins
name: build-configurable-deduplicated-and-lazy-plugins
category: computing-software
field: web-development
product: elysia
tags: [elysia, plugin, deduplication, lazy-load, config, functional-callback]
level: advanced
status: docs-checked
description: "Write Elysia plugins as instances or functions, pass config, deduplicate with name and seed, and register async or import-based plugins without blocking startup."
sources:
  - https://elysiajs.com/essential/plugin.html
  - https://elysiajs.com/key-concept.html
  - https://elysiajs.com/essential/best-practice.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: package reusable server pieces that compose without being applied twice.

## Plugin as instance

Any Elysia instance can be a plugin; register it with `.use(plugin)`. Types, state and decorators merge into the parent; lifecycle stays isolated unless scoped. Each instance can also run standalone. A plugin using another's service must declare that dependency with `.use()` itself.

## Config via factory function

```typescript
const version = (version = 1) => new Elysia().get('/version', version)
new Elysia().use(version(1)).listen(3000)
```

## Deduplication

By default a plugin runs again every time it is applied. Give it a unique `name` (plus optional `seed` that varies with config) and it is applied once:

```typescript
const ip = new Elysia({ name: 'ip' })
	.derive({ as: 'global' }, ({ server, request }) => ({ ip: server?.requestIP(request) }))

const plugin = (config) => new Elysia({ name: 'my-plugin', seed: config }).get(`${config.prefix}/hi`, () => 'Hi')
```

Named plugins act as singletons, so no performance worry from using them in many modules.

## Functional callback

`(app: Elysia) => app.state('counter', 0).get(...)` mutates the main instance directly, so it can inspect existing stores or routes (`'counter' in app.store`), but scope and encapsulation are harder to get right. The docs recommend a new instance instead; creating 10k instances takes milliseconds and inference is better.

## Lazy loading

Modules load eagerly by default. For heavy ones:

```typescript
// async plugin: registered after server start
export const loadStatic = async (app: Elysia) => { /* await work */ return app }
// lazy module
new Elysia().use(import('./plugin'))
```

To guarantee registration before the server starts, `await` the deferred module. In tests use `await app.modules` before calling `app.handle(...)`.

## Gotchas

- Without `name`, a shared plugin re-runs per `.use()`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (essential/plugin.html, key-concept.html, essential/best-practice.html); each claim, option name and default was compared with the page text. No changes were needed.

Method: documentation only; no commands were run.
