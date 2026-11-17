---
id: computing-software.web-development.nestjs.global-prefix-and-exclusions
name: global-prefix-and-exclusions
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, routing, global-prefix, versioning, http]
level: intro
status: docs-checked
description: "Set a NestJS global route prefix with setGlobalPrefix and exclude health or other routes using strings, route objects and named wildcards."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/global-prefix.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Prefix every route of an HTTP app:

```typescript
const app = await NestFactory.create(AppModule);
app.setGlobalPrefix('v1');
```

Exclude routes via the `exclude` option, either with an object (method specific) or a plain string (all methods):

```typescript
app.setGlobalPrefix('v1', {
  exclude: [{ path: 'health', method: RequestMethod.GET }],
});
app.setGlobalPrefix('v1', { exclude: ['cats'] });
```

`path` supports wildcard parameters through `path-to-regexp`. Bare `*` is deprecated; use `:param` or named wildcards `*splat`. A named wildcard needs at least one more segment, so `health/*splat` excludes `/health/status` but not `/health`. Wrap in braces to exclude both: `health/{*splat}`.

Excluded routes are registered outside the prefix, but Nest still handles unmatched requests to them. With `exclude: ['health']` and only a `GET /health` handler, `POST /health` goes through exception filters and gets Nest's standard 404.

Gotchas:
- With the Express adapter, a request to a path neither under the prefix nor excluded never reaches Nest: Express answers with its default 404 page. Fastify passes every unmatched request to Nest.
- With URI versioning, exclusions are matched without the version segment and an excluded route keeps it: `exclude: ['health']` with `defaultVersion: '1'` serves `/v1/health`.
## Checked

2026-11-04. Read the whole global prefix page (`content/faq/global-prefix.md` in nestjs/docs.nestjs.com). Confirmed `setGlobalPrefix()`, both `exclude` forms, the path-to-regexp wildcard hint (bare `*` deprecated, `*splat`, braces), the unmatched-request behaviour for excluded routes, the Express versus Fastify difference and the URI-versioning hint. Removed: the middleware `exclude()` gotcha (not on this page) and the invented Verify step.
Method: documentation only; no commands were run.
