---
id: computing-software.web-development.nestjs.async-providers
name: async-providers
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, providers, async, usefactory, database]
level: intro
status: docs-checked
description: "Delay NestJS startup until async work such as a database connection completes by using an async useFactory provider, and know the cold start cost."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/async-components.md
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/serverless.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `async`/`await` inside `useFactory`. Nest awaits the returned Promise before instantiating any class that depends on the provider, so the app does not start accepting requests until the connection exists.

```typescript
{
  provide: 'ASYNC_CONNECTION',
  useFactory: async () => {
    const connection = await createConnection(options);
    return connection;
  },
}
```

Inject it by token, like any other provider:

```typescript
constructor(@Inject('ASYNC_CONNECTION') private connection: Connection) {}
```

Serverless consideration: async providers delay bootstrap. If a function needs 2s on average to connect to the database, a cold start waits at least that long. For something used by only some invocations (the docs' example is a Redis cache), do not model it as an async provider; load the module lazily with `LazyModuleLoader` instead so other invocations start faster.

## Checked

2026-11-04. Read the whole asynchronous providers page (`content/fundamentals/async-components.md`) and the whole serverless page (`content/faq/serverless.md`) in nestjs/docs.nestjs.com. Confirmed the async `useFactory` example, awaiting before dependants are instantiated, injection by token, the 2s database example and the Redis/`LazyModuleLoader` advice. Removed: the claim to list the provider in `providers`/`exports` and to declare `inject: [...]` (not on these pages), the rejected-factory gotcha, and the Verify step.
Method: documentation only; no commands were run.
