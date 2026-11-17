---
id: computing-software.web-development.nestjs.lazy-loading-modules
name: lazy-loading-modules
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, lazy-loading, lazymoduleloader, serverless, performance]
level: advanced
status: docs-checked
description: "Load NestJS modules on demand with LazyModuleLoader to cut cold start time, and learn which constructs cannot be lazy loaded."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/lazy-loading-modules.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Modules load eagerly by default. For serverless functions and workers where cold start matters, `LazyModuleLoader` (from `@nestjs/core`) loads a module only when needed.

```typescript
@Injectable()
export class CatsService {
  constructor(private lazyModuleLoader: LazyModuleLoader) {}
}

const { LazyModule } = await import('./lazy.module.js');
const moduleRef = await this.lazyModuleLoader.load(() => LazyModule);

const { LazyService } = await import('./lazy.service.js');
const lazyService = moduleRef.get(LazyService);
```

You can also obtain it in `main.ts` with `app.get(LazyModuleLoader)`. `load()` returns the module reference of the lazy module and caches it: later calls take well under a millisecond (the docs show about 2.4ms first and 0.3ms after). A second argument `{ logger: false }` suppresses load logs. The lazy module is a regular Nest module and shares the module graph with eagerly loaded ones.

Typical use: a worker, cron job, lambda or webhook that must run different logic depending on input.

Gotchas:
- Lifecycle hooks are not invoked in lazy loaded modules and services.
- Lazy modules cannot be global, and global enhancers (guards, interceptors) will not work properly.
- Controllers, resolvers and gateways cannot be lazy loaded, and neither can middleware via `configure()`. Fastify cannot add routes after listening; Kafka, gRPC and RabbitMQ transports must subscribe before connecting; code-first GraphQL needs all classes loaded to build the schema.
- With webpack set `compilerOptions.module` to `esnext` and `moduleResolution` to `node` in `tsconfig.json` to enable code splitting.
- It makes little sense for monoliths where startup time is irrelevant.

Verify: log timing around two `load()` calls; the second should be much faster.

## Checked

2026-11-04. Read the whole lazy loading modules page (`content/fundamentals/lazy-loading-modules.md` in nestjs/docs.nestjs.com). Confirmed eager loading by default, `LazyModuleLoader` and its import, `load()` and `moduleRef.get()`, caching and the sample timings, the `logger: false` option, the shared module graph, the global-module and enhancer limits, the lifecycle hook warning, the webpack `tsconfig.json` settings, the controller, gateway, resolver and middleware limits with the Fastify, Kafka, gRPC, RabbitMQ and code-first GraphQL reasons, and the use cases. Nothing removed. The Verify step is kept because the page shows the faster cached attempts.
Method: documentation only; no commands were run.
