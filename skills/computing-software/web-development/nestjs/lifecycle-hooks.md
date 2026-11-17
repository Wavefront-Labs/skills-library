---
id: computing-software.web-development.nestjs.lifecycle-hooks
name: lifecycle-hooks
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, lifecycle, hooks, oninit, bootstrap]
level: practitioner
status: docs-checked
description: "Run code at NestJS startup and shutdown with onModuleInit, onApplicationBootstrap and the destroy hooks, including async init and ordering rules."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/lifecycle-events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nest calls hook methods on modules, providers and controllers. Implement the interface for typing (interfaces are optional at runtime).

| Hook | When |
| --- | --- |
| `onModuleInit()` | host module's dependencies resolved |
| `onApplicationBootstrap()` | all modules initialized, before listening |
| `onModuleDestroy()` | after a termination signal |
| `beforeApplicationShutdown()` | after all `onModuleDestroy()` handlers finish |
| `onApplicationShutdown()` | after connections close |

```typescript
@Injectable()
export class UsersService implements OnModuleInit {
  async onModuleInit(): Promise<void> {
    await this.fetch();
  }
}
```

Returning a Promise (or using `async`) in `onModuleInit` and `onApplicationBootstrap` defers initialization until it resolves.

Ordering: hooks run module by module, ordered by distance from the root in the import graph: the most deeply imported modules (and global modules) first, the root last, each awaited before the next. Shutdown hooks run in reverse.

Init hooks run on `app.init()`, `app.listen()`, or `NestFactory.createApplicationContext()`. Destroy hooks run only on an explicit `app.close()` or on a system signal after `enableShutdownHooks()`.

Gotcha: lifecycle hooks are not triggered for request-scoped classes, since their lifespan is per request.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: hook table, async init, ordering hint, init and destroy triggers, request-scoped warning (lifecycle-events page). Removed: invented Verify step.

Method: documentation only; no commands were run.
