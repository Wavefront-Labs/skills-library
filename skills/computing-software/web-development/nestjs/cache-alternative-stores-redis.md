---
id: computing-software.web-development.nestjs.cache-alternative-stores-redis
name: cache-alternative-stores-redis
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, caching, redis, keyv, registerasync]
level: advanced
status: docs-checked
description: "Back NestJS CacheModule with Redis and an in-memory layer via Keyv stores, and configure it asynchronously with registerAsync."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/data/caching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Install `npm install @keyv/redis cacheable`. Register several stores; the first is the default and the rest are fallbacks:

```typescript
CacheModule.registerAsync({
  useFactory: async () => {
    const redisStore = createKeyv('redis://localhost:6379');
    redisStore.on('error', (err) => console.error('Redis error:', err));
    return {
      stores: [
        new Keyv({ store: new KeyvCacheableMemory({ ttl: 60000, lruSize: 5000 }) }),
        redisStore,
      ],
    };
  },
}),
```

Imports: `createKeyv` from `@keyv/redis`, `Keyv` from `keyv`, `KeyvCacheableMemory` from `cacheable`.

Async options mirror other Nest modules:

```typescript
CacheModule.registerAsync({
  imports: [ConfigModule],
  useFactory: async (configService: ConfigService) => ({ ttl: configService.get('CACHE_TTL') }),
  inject: [ConfigService],
});
```

Alternatives: `useClass: CacheConfigService` (implement `CacheOptionsFactory.createCacheOptions(): CacheModuleOptions`), `useExisting: ConfigService` (reuses an imported instance), and `extraProviders: [MyAdditionalProvider]`. `register`, `registerAsync` and `CacheOptionsFactory` accept a generic to type store-specific options.

Gotchas:
- Always attach an `'error'` listener to the Redis store. A dropped connection emits `error`, and Keyv throws if nothing listens, which can crash the app.
- Keyv stores serialize to JSON, so class instances come back as plain objects and `Date` becomes a string.

## Checked

2026-11-04. Read the whole caching page (`content/data/caching.md` in nestjs/docs.nestjs.com). Confirmed the install line, the multi-store `registerAsync` example and imports, first-store-is-default, the Redis `'error'` listener warning, JSON serialization of Keyv stores, `useFactory`/`inject`, `useClass`/`CacheOptionsFactory`, `useExisting`, `extraProviders` and the generic type argument. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
