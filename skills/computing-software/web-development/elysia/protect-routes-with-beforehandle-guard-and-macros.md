---
id: computing-software.web-development.elysia.protect-routes-with-beforehandle-guard-and-macros
name: protect-routes-with-beforehandle-guard-and-macros
category: computing-software
field: web-development
product: elysia
tags: [elysia, life-cycle, before-handle, guard, macro, authorization]
level: practitioner
status: docs-checked
description: "Reject unauthorized requests in Elysia with beforeHandle, apply it to many routes with guard, and package auth and schema as a reusable macro."
sources:
  - https://elysiajs.com/essential/life-cycle.html
  - https://elysiajs.com/essential/plugin.html
  - https://elysiajs.com/tutorial/patterns/macro/
  - https://elysiajs.com/tutorial/getting-started/guard/
  - https://elysiajs.com/key-concept.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run an access check after validation and short-circuit with a 401.

## beforeHandle

Runs after validation and before the handler. If it returns a value, the handler is skipped and that value becomes the response.

```typescript
new Elysia().get('/', () => 'hi', {
	beforeHandle({ cookie: { session }, status }) {
		if (!validateSession(session.value)) return status(401)
	}
})
```

## guard for many routes

```typescript
new Elysia()
	.guard(
		{ beforeHandle({ cookie: { session }, status }) { if (!validateSession(session.value)) return status(401) } },
		(app) => app.get('/user/:id', handler).post('/profile', handler2, { beforeHandle: isUserExists })
	)
	.get('/', () => 'hi')   // not guarded
```

`guard` also accepts schemas and several hooks, including arrays (`beforeHandle: [a, b]`). Without a callback (`.guard({...})`) it applies to every route registered after it in the same instance.

## Macro: a reusable route option

```typescript
new Elysia()
	.macro('auth', {
		cookie: t.Object({ session: t.String() }),
		beforeHandle({ cookie: { session }, status }) {
			if (!session.value) return status(401)
		}
	})
	.post('/user', ({ body }) => body, { auth: true })
```

`auth: true` inlines both the cookie schema and the beforeHandle into the route, with type soundness. A macro can also set `body` to enforce a type, then short-circuit with `status` (the tutorial's Fibonacci example returns `status(418)`).

## Gotchas

- Hooks inside a plugin do not leak to the parent unless scoped (`{ as: 'global' }` or `.as('scoped')`).
- The plugin page lists macro among plugins that add types, which it recommends as explicit dependencies (`.use()` them where needed).

## Checked

2026-11-07. Read in full: essential/life-cycle, essential/plugin, tutorial/patterns/macro, tutorial/getting-started/guard and key-concept. Confirmed `beforeHandle` short-circuiting, `guard` with a callback, `guard` taking schemas and hooks including a `beforeHandle` array and applying to routes after `.guard` without a callback, the `auth` macro inlining `cookie` and `beforeHandle`, the Fibonacci `body` plus `status(418)` example, and plugin scoping. Removed an invented Verify step and a gotcha claiming `return status(401)` is needed for Eden typing (not on these pages); reworded the plugin-sharing gotcha to what the plugin page states.

Method: documentation only; no commands were run.
