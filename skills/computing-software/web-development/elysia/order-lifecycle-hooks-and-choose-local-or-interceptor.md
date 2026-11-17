---
id: computing-software.web-development.elysia.order-lifecycle-hooks-and-choose-local-or-interceptor
name: order-lifecycle-hooks-and-choose-local-or-interceptor
category: computing-software
field: web-development
product: elysia
tags: [elysia, life-cycle, hooks, local-hook, interceptor, order-of-code]
level: practitioner
status: docs-checked
description: "Pick the right Elysia lifecycle event, choose a local hook or an interceptor hook, and place hooks before the routes they must affect."
sources:
  - https://elysiajs.com/essential/life-cycle.html
  - https://elysiajs.com/key-concept.html
  - https://elysiajs.com/tutorial/getting-started/life-cycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: attach logic at the correct stage of request handling, and have it apply to the intended routes.

## Event order

Request, Parse, Transform (derive lives here), Validation, Before Handle (resolve lives here), the handler, After Handle, Map Response, After Response; On Error catches errors thrown in any stage; Trace audits timing. Hook names are camelCase: `onRequest`, `onParse`, `onTransform`, `onBeforeHandle`, `onAfterHandle`, `onMapResponse` (`mapResponse`), `onError`, `onAfterResponse`.

## Two hook kinds

Local hook: the third argument of a route, affects that route only.

```typescript
.get('/auth', () => 'ok', {
	beforeHandle({ status }) { if (Math.random() <= 0.5) return status(418) }
})
```

Interceptor hook: `.onX(...)` affects every route of the current instance registered after it.

```typescript
new Elysia()
	.get('/none', () => '<h1>Hi</h1>')            // no hook
	.onAfterHandle(({ responseValue, set }) => { /* ... */ })
	.get('/', () => '<h1>Hi</h1>')                // hook applies
```

A hook receives the same context as a handler.

## Order of code

Events apply only to routes registered after them, and the same holds for plugins: `onBeforeHandle(log 1) -> .use(someRouter) -> onBeforeHandle(log 2)` logs only `1` for the plugin's routes. The one exception is `onRequest`, which is global because it runs before a route is known.

## Which event for what

- onRequest: caching, rate limiting, IP or region lock, analytics, CORS headers; returning a value skips the rest of the lifecycle. Its context is the minimal PreContext (request, set, store, decorators; no derived values).
- beforeHandle: authorization and custom checks; a returned value skips the handler.
- afterHandle / mapResponse: change or map the result.
- afterResponse: cleanup, logging.

## Gotchas

- Interceptor hooks are scoped to the current instance; a hook inside a plugin does not reach the parent unless you set its scope (the key-concept page uses `{ as: 'global' }`).
- `resolve` and `onBeforeHandle` share one queue and run in registration order (the life-cycle page logs 1, 2, 3); `derive` and `transform` likewise share a queue.

## Checked

2026-11-07. Read in full: essential/life-cycle, key-concept and tutorial/getting-started/life-cycle. Confirmed the event list and order, hook names, local versus interceptor hooks, order of code with the 1/2 log example (including the plugin case and the `onRequest` exception), `onRequest` use cases and `PreContext`, and `beforeHandle` skipping the handler. Replaced two unsupported gotchas (a "matters more than where the plugin is defined" claim and a `beforeHandle: [fnA, fnB]` guard-array claim, neither on these pages) with the encapsulation and shared-queue facts the pages state.

Method: documentation only; no commands were run.
