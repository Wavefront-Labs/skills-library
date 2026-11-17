---
id: computing-software.web-development.elysia.reuse-schemas-with-reference-models-and-standalone-guards
name: reuse-schemas-with-reference-models-and-standalone-guards
category: computing-software
field: web-development
product: elysia
tags: [elysia, validation, model, reference-model, standalone, guard]
level: advanced
status: docs-checked
description: "Reuse Elysia schemas as named reference models with model, avoid name clashes, and make a guard schema co-exist with route schemas using standalone."
sources:
  - https://elysiajs.com/essential/validation.html
  - https://elysiajs.com/tutorial/patterns/standalone-schema/
  - https://elysiajs.com/essential/best-practice.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: define a schema once, reference it by name, and control how guard schemas merge with route schemas.

## Reference model

```typescript
const app = new Elysia()
	.model({ sign: t.Object({ username: t.String(), password: t.String() }) })
	.post('/sign-in', ({ body }) => body, { body: 'sign', response: 'sign' })
```

Names get auto-completion. `model` accepts several models in one object. Put models in their own instance and `.use()` it:

```typescript
export const authModel = new Elysia().model({ sign: t.Object({...}), number: t.Number() })
new Elysia().use(authModel).post('/sign-in', handler, { body: 'sign' })
```

Benefits: named schemas, can be remapped (`.prefix('model', 'auth.')`), shown as models/components in OpenAPI, and faster TypeScript inference because types are cached at registration.

## Naming

Duplicate model names make Elysia throw. Prefix by module: `'admin.auth'`, `'user.auth'`. The team should settle a convention.

## Plain constants

Without registration you can simply share a const (`const SignDTO = t.Object({...})`) in `body` and `response`.

## Guard schema merging

Default `schema: 'override'`: a route schema replaces a colliding guard schema, and the latest guard wins. With `schema: 'standalone'` both are validated independently:

```typescript
new Elysia()
	.guard({ schema: 'standalone', body: t.Object({ age: t.Number() }) })
	.post('/user', ({ body }) => body, { body: t.Object({ name: t.String() }) })
	// body must contain both age and name
```

Standalone schemas may use different libraries: a zod guard plus an `Elysia.t` route schema works together.

## Gotchas

- `.prefix('model', 'auth.')` changes referenced names (the docs use `'auth.Sign'`), so keep naming consistent.

## Checked

2026-11-07. Read in full: essential/validation (Guard Schema Type, Reference Model, Multiple Models, Naming Convention), tutorial/patterns/standalone-schema and essential/best-practice (Model Injection). Confirmed `model` registration and auto-completion, model plugins, duplicate-name error and namespaced names, the four listed benefits (including `.prefix('model', 'auth.')`), override versus standalone guard schemas, and zod plus `Elysia.t` interoperability. Nothing removed.

Method: documentation only; no commands were run.
