---
id: computing-software.web-development.nestjs.api-versioning-controllers-routes
name: api-versioning-controllers-routes
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, versioning, version-neutral, defaultversion, controllers]
level: practitioner
status: docs-checked
description: "Assign NestJS versions to controllers and routes with Controller version, the Version decorator, arrays, VERSION_NEUTRAL, defaultVersion and middleware."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/http/versioning.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Controller version:

```typescript
@Controller({ version: '1' })
export class CatsControllerV1 {
  @Get('cats') findAll(): string { return 'v1'; }
}
```

Route version (overrides the controller version):

```typescript
@Controller()
export class CatsController {
  @Version('1') @Get('cats') findAllV1() {}
  @Version('2') @Get('cats') findAllV2() {}
}
```

Multiple versions: `version: ['1', '2']`. Version neutral (matches any version or none; with URI versioning its URL has no version segment): `version: VERSION_NEUTRAL`, imported from `@nestjs/common`.

Global default:

```typescript
app.enableVersioning({ type: VersioningType.URI, defaultVersion: '1' /* or ['1','2'] or VERSION_NEUTRAL */ });
```

Middleware: `consumer.apply(LoggerMiddleware).forRoutes({ path: 'cats', method: RequestMethod.GET, version: '2' })`.

Gotchas:
- With versioning enabled but no version and no `defaultVersion`, a controller behaves like `VERSION_NEUTRAL`. With URI versioning it is served only at `/cats`, and `/v1/cats` returns 404.
- Register neutral or unversioned routes after versioned ones sharing a path (later in `controllers`, lower in the class, or in a later module). Under Express with non-URI versioning, routes with the same path are tried in registration order, so a neutral route registered first also answers requests meant for versioned ones.
- A module's own controllers register before those of its imports.

Verify: request `/cats` and `/v1/cats` and check which one 404s.

## Checked

2026-11-04. Read the whole versioning page (`content/http/versioning.md` in nestjs/docs.nestjs.com). Confirmed controller and route versions, route override, arrays, `VERSION_NEUTRAL`, `defaultVersion`, middleware `version`, the no-version behaviour, and the registration-order notice. Nothing removed.
Method: documentation only; no commands were run.
