---
id: computing-software.web-development.nestjs.cache-module-and-interceptor
name: cache-module-and-interceptor
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, caching, cache-manager, cacheinterceptor, ttl]
level: practitioner
status: docs-checked
description: "Cache NestJS data with CacheModule, the CACHE_MANAGER token, CacheInterceptor, CacheKey, CacheTTL and a custom trackBy."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/data/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm install @nestjs/cache-manager cache-manager`. Register (in-memory by default):

```typescript
@Module({
  imports: [CacheModule.register({ ttl: 5000, isGlobal: true })],
})
export class AppModule {}
```

`ttl` is in milliseconds; unset or `0` means entries never expire.

Manual use:

```typescript
constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}
const value = await this.cacheManager.get('key');
await this.cacheManager.set('key', 'value', 1000);
await this.cacheManager.del('key');
await this.cacheManager.clear();
```

`Cache` and `CACHE_MANAGER` come from `@nestjs/cache-manager`. A miss returns `undefined` (v6 returned `null`; treat both as a miss when migrating).

Auto-caching: `@UseInterceptors(CacheInterceptor)` on a controller, or globally via `{ provide: APP_INTERCEPTOR, useClass: CacheInterceptor }`. Override per route with `@CacheKey('custom_key')` and `@CacheTTL(2000)`; `@CacheTTL(5000)` on the controller is the default for its routes and method-level wins. To track by something other than the URL (for example the `Authorization` header), subclass the interceptor and override `trackBy(context: ExecutionContext): string | undefined`.

Gotchas:
- Only `GET` endpoints are cached (an explicit `@CacheKey()` bypasses this). Routes injecting `@Res()` cannot use the interceptor.
- It does not work properly in GraphQL, because interceptors run per field resolver.
- For WebSocket and microservice handlers `@CacheKey()` is required, otherwise nothing is cached.
- The in-memory store returns the same object reference you set, so mutating it mutates the cache.
- Do not cache actions that perform business operations.

## Checked

2026-11-04. Read the whole caching page (`content/data/caching.md` in nestjs/docs.nestjs.com). Confirmed the install line, `register` options `ttl` (milliseconds, unset or `0` never expires) and `isGlobal`, `CACHE_MANAGER` and `Cache` imports, `get`/`set`/`del`/`clear`, the `undefined` miss versus v6 `null`, `CacheInterceptor` (controller and `APP_INTERCEPTOR`), `@CacheKey`/`@CacheTTL` precedence, `trackBy`, and every gotcha listed. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
