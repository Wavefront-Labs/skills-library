---
id: computing-software.web-development.nestjs.api-versioning-types
name: api-versioning-types
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, versioning, enableversioning, uri, header, media-type]
level: practitioner
status: docs-checked
description: "Enable NestJS API versioning by URI, header, media type or a custom extractor with enableVersioning and VersioningType."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/http/versioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
HTTP apps only. Enable with `app.enableVersioning({ ... })`; `VersioningType` is imported from `@nestjs/common`.

URI (default style, `/v1/route`; the version is placed after the global prefix and before controller paths; the `v` prefix is configurable with `prefix`, or `false`):

```typescript
app.enableVersioning({ type: VersioningType.URI });
```

Header:

```typescript
app.enableVersioning({ type: VersioningType.HEADER, header: 'Custom-Header' });
```

Media type, for `Accept: application/json;v=2` the key includes the separator:

```typescript
app.enableVersioning({ type: VersioningType.MEDIA_TYPE, key: 'v=' });
```

Custom: provide an `extractor` returning a string or an array sorted highest to lowest.

```typescript
const extractor = (request: FastifyRequest): string | string[] =>
  [request.headers['custom-versioning-field'] ?? '']
    .flatMap(v => v.split(','))
    .filter(v => !!v)
    .sort()
    .reverse();
app.enableVersioning({ type: VersioningType.CUSTOM, extractor });
```

With extracted versions `['3','2','1']` and routes only for `2` and `1`, version `2` is chosen. An empty result matches no versioned route (404), while `VERSION_NEUTRAL` routes still match.

Gotchas:
- With the Express adapter make the extractor return a single version; highest-match selection from a multi-element array does not reliably work there. Fastify supports it.
- Middleware `version` targeting works only when each version has its own path (URI). With header, media type or custom versioning, use a guard or interceptor for one version.

## Checked

2026-11-04. Read the whole versioning page (`content/http/versioning.md` in nestjs/docs.nestjs.com). Confirmed the four types and their options (`type`, `header`, `key`, `extractor`, `prefix`), the `v` default prefix, extractor ordering and the `['3','2','1']` example, the empty-result 404 behaviour, the Express versus Fastify notice and the middleware notice. Removed the Verify line (the page does not describe such a check).
Method: documentation only; no commands were run.
