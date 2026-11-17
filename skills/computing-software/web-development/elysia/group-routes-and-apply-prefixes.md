---
id: computing-software.web-development.elysia.group-routes-and-apply-prefixes
name: group-routes-and-apply-prefixes
category: computing-software
field: web-development
product: elysia
tags: [elysia, route, group, prefix, guard, plugin]
level: practitioner
status: docs-checked
description: "Share a URL prefix across Elysia routes with group, group plus a guard schema, or a plugin instance created with the prefix constructor option."
sources:
  - https://elysiajs.com/essential/route.html
  - https://elysiajs.com/essential/plugin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: avoid repeating `/user/...` on every route and optionally attach a schema to the whole set.

## group

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.group('/user', (app) =>
		app
			.post('/sign-in', 'Sign in')
			.post('/sign-up', 'Sign up')
			.post('/profile', 'Profile')
	)
```

Result: `/user/sign-in`, `/user/sign-up`, `/user/profile`.

## group with a guard schema

`group` accepts three parameters: prefix, guard, then the callback. This replaces nesting `group` and `guard`.

```typescript
import { Elysia, t } from 'elysia'

new Elysia().group(
	'/v1',
	{ body: t.Literal('Rikuhachima Aru') },
	(app) => app.post('/student', ({ body }) => body)
)
```

## prefix constructor option

Split the group into its own plugin instance to cut nesting:

```typescript
const users = new Elysia({ prefix: '/user' })
	.post('/sign-in', 'Sign in')
	.post('/sign-up', 'Sign up')
	.post('/profile', 'Profile')

new Elysia().use(users).get('/', 'hello world').listen(3000)
```

## Guard without a prefix

`guard(schemaOrHooks, (app) => ...)` applies the same schema and hooks to the routes inside the callback only; routes outside (for example `/`) are not validated. Guard takes the same parameters as an inline hook.

## Gotchas

- Hooks registered inside a plugin are not inherited by the parent unless you set a scope (`{ as: 'global' }` or `.as('scoped')`).

## Checked

2026-11-07. Read in full: essential/route (Group and Prefix sections) and essential/plugin (Guard, Grouped Guard, Scope). Confirmed `group('/user', ...)` results, the three-parameter group with a guard schema, `new Elysia({ prefix })` with `.use`, and guard applying only inside its callback. Removed an invented Verify step and a gotcha that a group callback must return the app (not stated on the pages).

Method: documentation only; no commands were run.
