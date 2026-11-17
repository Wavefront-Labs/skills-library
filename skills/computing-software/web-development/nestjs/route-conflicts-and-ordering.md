---
id: computing-software.web-development.nestjs.route-conflicts-and-ordering
name: route-conflicts-and-ordering
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, routing, express, fastify, conflicts]
level: practitioner
status: docs-checked
description: "Detect and fix NestJS routes shadowed by parametric routes using declaration order, routeConflictPolicy and routeResolutionStrategy options."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/controllers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nest registers routes in declaration order. On order-sensitive adapters, notably the default Express adapter, a parametric route silently shadows a more specific one:

```typescript
@Controller('users')
export class UsersController {
  @Get(':id')
  findOne() {}

  @Get('me') // never reached: `:id` matches "me" first
  findMe() {}
}
```

The app boots without a warning and requests go to the wrong handler. Pipes such as `ParseIntPipe` cannot help because routing picks the handler before any pipe runs.

The simple fix is to declare static paths before parameterized ones.

NestJS v12 adds two opt-in `NestApplicationOptions` (defaults keep old behavior):

```typescript
const app = await NestFactory.create(AppModule, {
  routeConflictPolicy: { duplicate: 'error', shadow: 'warn' },
  routeResolutionStrategy: 'specificity',
});
```

- `routeConflictPolicy` takes `duplicate` (identical method, path, host and version) and `shadow` (two patterns can match the same request), each `'off'` (default), `'warn'` or `'error'`. With `'error'`, all offending pairs are aggregated into one `RouteConflictException` thrown at `app.init()` (or `app.listen()` if init is not called explicitly).
- `routeResolutionStrategy: 'specificity'` registers literal segments before parametric ones before wildcards. Default is `'declaration'`.

The types `RouteConflictPolicy`, `RouteConflictPolicyLevel` and `RouteResolutionStrategy` are exported from `@nestjs/common`.

Gotcha: `FastifyAdapter` is not order-sensitive (find-my-way ranks by specificity), so `shadow` is a no-op and `'specificity'` has no effect there; the `duplicate` policy works on both adapters.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: shadowing example, routeConflictPolicy levels and conflict kinds, RouteConflictException timing, routeResolutionStrategy, Fastify behaviour, exported types (controllers page, Route conflicts section). Removed: invented Verify step.

Method: documentation only; no commands were run.
