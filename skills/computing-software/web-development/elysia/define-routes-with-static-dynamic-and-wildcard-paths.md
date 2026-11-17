---
id: computing-software.web-development.elysia.define-routes-with-static-dynamic-and-wildcard-paths
name: define-routes-with-static-dynamic-and-wildcard-paths
category: computing-software
field: web-development
product: elysia
tags: [elysia, route, params, wildcard, http-methods, custom-method]
level: intro
status: docs-checked
description: "Define Elysia routes using HTTP verb methods, static, dynamic, optional and wildcard paths, custom methods with route and any-method routes with all."
sources:
  - https://elysiajs.com/essential/route.html
  - https://elysiajs.com/tutorial/getting-started/your-first-route/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: map method plus path to a handler and know which route wins when several match.

A route is a method named after the HTTP verb, a path, a handler, and optional hook (metadata) object: `.get(path, handler, hook)`.

```typescript
import { Elysia } from 'elysia'

new Elysia()
	.get('/id/1', 'static path')
	.get('/id/:id', 'dynamic path')
	.get('/id/*', 'wildcard path')
	.listen(3000)
```

## Path types

- Static: hard-coded string, `/hello`.
- Dynamic: colon plus name, `/id/:id`; read with `({ params: { id } }) => id`. Several are allowed: `/id/:id/:name`.
- Optional parameter: add `?` after the name, `/id/:id?`, so a static and a dynamic path can resolve the same handler.
- Wildcard: `*` captures the rest of the path, read as `params['*']`.

`/id/:id` matches `/id/1` and ignores a query string (`/id/anything?name=salt` gives `anything`), but `/id` and `/id/anything/rest` are Not Found.

## Priority

1. static, 2. dynamic, 3. wildcard. With the three routes above, `/id/1` returns "static path", `/id/2` "dynamic path", `/id/2/a` "wildcard path".

## Verbs, custom methods, all

Built-in methods include `get`, `post`, `put`, `patch`, `delete`. For other verbs use `route(method, path, handler, hook)`:

```typescript
.route('M-SEARCH', '/m-search', 'connect')
```

HTTP verbs are case-sensitive (RFC 7231); use UPPERCASE for custom ones. `.all('/', 'hi')` handles any method on that path.

## Verify programmatically

`app.handle(new Request('http://localhost/'))` returns a Promise of a Response, processed like a real request, without starting a server.

## Gotchas

- A handler may be a literal value (`.get('/', 'hello')`).

## Checked

Checked 2026-11-07 against the Elysia documentation source (essential/route.html, tutorial/getting-started/your-first-route/); each claim, option name and default was compared with the page text. Removed the claim that /id resolves with id undefined (mock only) and the params-are-strings claim.

Method: documentation only; no commands were run.
