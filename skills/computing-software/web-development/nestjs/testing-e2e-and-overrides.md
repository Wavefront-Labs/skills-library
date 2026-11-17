---
id: computing-software.web-development.nestjs.testing-e2e-and-overrides
name: testing-e2e-and-overrides
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, testing, e2e, supertest, overrideprovider]
level: advanced
status: docs-checked
description: "Write NestJS end-to-end tests with Supertest, override providers, guards and modules, replace global APP_GUARD enhancers, and test request-scoped providers."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/unit-testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
E2E tests live in `test/` with an `.e2e-spec` suffix and drive a full app:

```typescript
const moduleRef = await Test.createTestingModule({ imports: [CatsModule] })
  .overrideProvider(CatsService)
  .useValue(catsService)
  .compile();

app = moduleRef.createNestApplication();
await app.init();

await request(app.getHttpServer()).get('/cats').expect(200);
// afterAll: await app.close();
```

Overrides: `overrideProvider()`, `overrideGuard()`, `overrideInterceptor()`, `overrideFilter()`, `overridePipe()`, each returning `useClass`, `useValue` and `useFactory` (an object with `factory` and optional `inject`). `overrideModule(CatsModule).useModule(AlternateCatsModule)` swaps modules. Chain them before `compile()`.

Fastify: create with `createNestApplication<NestFastifyApplication>(new FastifyAdapter())`, then `await app.init()` and `await app.getHttpAdapter().getInstance().ready()`, and test with `app.inject({ method: 'GET', url: '/cats' })`.

Overriding a global guard: `{ provide: APP_GUARD, useClass: JwtAuthGuard }` is not overridable. Register it as an alias to a regular provider:

```typescript
providers: [
  { provide: APP_GUARD, useExisting: JwtAuthGuard },
  JwtAuthGuard,
],
// test
.overrideProvider(JwtAuthGuard).useClass(MockAuthGuard)
```

Request-scoped instances: fix the context id so you can resolve the same sub-tree:

```typescript
const contextId = ContextIdFactory.create();
vi.spyOn(ContextIdFactory, 'getByRequest').mockImplementation(() => contextId);
catsService = await moduleRef.resolve(CatsService, contextId);
```

Gotcha: after `compile()` alone, `HttpAdapterHost#httpAdapter` is undefined; use `createNestApplication()` when a test needs it. Other module methods: `createNestMicroservice()`, `select()`.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: e2e setup, override methods and useModule, Fastify inject, APP_GUARD useExisting, request-scoped ContextIdFactory spy, HttpAdapterHost caveat (unit-testing page). Removed: invented Verify step.

Method: documentation only; no commands were run.
