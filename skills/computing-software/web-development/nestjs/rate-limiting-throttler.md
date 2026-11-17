---
id: computing-software.web-development.nestjs.rate-limiting-throttler
name: rate-limiting-throttler
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, rate-limiting, throttler, security, guards]
level: practitioner
status: docs-checked
description: "Protect NestJS routes from brute force with @nestjs/throttler: ThrottlerModule.forRoot, ThrottlerGuard, named limits, Throttle and SkipThrottle."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/security/rate-limiting.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm i --save @nestjs/throttler`.

```typescript
ThrottlerModule.forRoot([
  { name: 'short', ttl: 1000, limit: 3 },
  { name: 'medium', ttl: 10000, limit: 20 },
  { name: 'long', ttl: 60000, limit: 100 },
]),
```

`ttl` is in milliseconds (since v5). Single set form: `forRoot({ throttlers: [{ ttl: 60000, limit: 10 }] })`. Bind the guard globally:

```typescript
{ provide: APP_GUARD, useClass: ThrottlerGuard }
```

Per route or class:
- `@Throttle({ default: { limit: 3, ttl: 60000 } })` overrides limits (use the set name as key, `default` if unnamed; optional `blockDuration`).
- `@SkipThrottle()` skips a class or route; `@SkipThrottle({ default: false })` re-enables a route inside a skipped class.

Options per set: `name`, `ttl`, `limit`, `blockDuration` (defaults to `ttl`), `ignoreUserAgents`, `skipIf(context)`, `getTracker`, `generateKey`, `setHeaders` (named sets append the name, such as `X-RateLimit-Remaining-long`). Module level adds `storage`, `errorMessage` and `ipv6SubnetPrefix` (default 64). Use `forRootAsync({ imports, inject, useFactory: (config) => [{ ttl, limit }] })` for config-driven values. Helpers `seconds()`, `minutes()`, `hours()`, `days()`, `weeks()` return milliseconds.

Storage is in-memory by default; implement `ThrottlerStorage` or use a Redis storage for multiple instances.

Gotchas:
- Migrating from v4: ttl was seconds, now milliseconds.
- GraphQL needs a guard override of `getRequestResponse()` using `GqlExecutionContext`.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: forRoot forms, named throttlers, ttl in milliseconds, APP_GUARD, Throttle and SkipThrottle, option tables with defaults, forRootAsync, time helpers, storage, GraphQL override, v5 migration (rate-limiting page). Removed: invented Verify step.

Method: documentation only; no commands were run.
