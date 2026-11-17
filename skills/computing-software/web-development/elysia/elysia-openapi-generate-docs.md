---
id: computing-software.web-development.elysia.elysia-openapi-generate-docs
name: elysia-openapi-generate-docs
category: computing-software
field: web-development
product: elysia
tags: [openapi, swagger, scalar, documentation, plugin]
level: practitioner
status: docs-checked
description: "Generate an API reference page and OpenAPI JSON for an Elysia app with @elysia/openapi, hide or exclude routes, and migrate from @elysia/swagger."
sources:
  - https://elysiajs.com/plugins/openapi.html
  - https://elysiajs.com/plugins/swagger.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: publish interactive API docs generated from your route schemas.

1. Install: `bun add @elysia/openapi`
2. Use it:

```typescript
import { Elysia } from 'elysia'
import { openapi } from '@elysia/openapi'

new Elysia()
    .use(openapi())
    .get('/', () => 'hello')
    .post('/hello', () => 'OpenAPI')
    .listen(3000)
```

`/openapi` serves a Scalar UI; the raw spec is at `/openapi/json`.

Plugin config (defaults from the docs):
- `enabled` (true), `documentation` (OpenAPI document info, OpenAPI 3.0.3 spec), `path` (`'/openapi'`), `specPath` (`'/${path}/json'`), `provider` (`'scalar'`; or SwaggerUI; `null` disables the frontend), `scalar` and `swagger` (passed to those UIs), `references`, `mapJsonSchema`.
- `exclude`: `methods`, `paths`, `tags`, and `staticFile` (default true: static file routes are excluded).
- `mapJsonSchema` maps other standard-schema libraries to JSON schema, e.g. `openapi({ mapJsonSchema: { valibot: toJsonSchema } })` with `toJsonSchema` from `@valibot/to-json-schema`.
- Self-host Scalar: `openapi({ scalar: { cdn: '/public/scalar-standalone.min.js', withDefaultFonts: false } })`. `cdn` is an Elysia plugin option, not a Scalar one.

Per-route docs go in the route's `detail` object (extends the OpenAPI Operation Object): `hide` (true removes the route from the page), `deprecated` (default false), `description`, `summary`. Example: `.post('/sign-in', handler, { body: t.Object({...}), detail: { hide: true } })`.

Migrating from the deprecated `@elysia/swagger` (docs say it is no longer maintained): that plugin was `swagger()` at `/swagger` (spec at `/swagger/json`) with options `provider` (default `scalar`), `scalar`, `swagger`, `excludeStaticFile` (default true), `path` (default `/swagger`), `exclude` (string, RegExp or array). The swagger page shows these patterns via `documentation`: tags (`documentation: { tags: [{ name: 'App', description: 'General endpoints' }] }` and `detail: { tags: ['App'] }` per route) and Bearer security (`documentation.components.securitySchemes.bearerAuth = { type: 'http', scheme: 'bearer', bearerFormat: 'JWT' }` plus `detail: { security: [{ bearerAuth: [] }] }` on a prefixed `new Elysia({ prefix: '/address', detail: {...} })`). The openapi page does not show the tag or Bearer samples.

Gotchas: exclusion option names differ between the plugins (`exclude.staticFile` vs `excludeStaticFile`), and the default path changed from `/swagger` to `/openapi`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/openapi.html, plugins/swagger.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and an unresolved migration caveat; noted which samples only the swagger page shows.

Method: documentation only; no commands were run.
