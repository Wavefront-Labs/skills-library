---
id: computing-software.web-development.nestjs.graceful-shutdown-hooks
name: graceful-shutdown-hooks
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, shutdown, signals, kubernetes, lifecycle]
level: practitioner
status: docs-checked
description: "Enable NestJS shutdown hooks so SIGTERM triggers onModuleDestroy, beforeApplicationShutdown and onApplicationShutdown, with Windows and test caveats."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/fundamentals/lifecycle-events.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Shutdown hooks are disabled by default because the signal listeners consume resources. Opt in at bootstrap:

```typescript
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableShutdownHooks();
  await app.listen(process.env.PORT ?? 3000);
}
```

On a termination signal Nest calls `onModuleDestroy()`, `beforeApplicationShutdown()` and `onApplicationShutdown()` in that order. The last two receive the signal as first parameter (`onModuleDestroy()` takes none). If a hook returns a Promise, Nest waits for it to resolve or reject before continuing.

```typescript
@Injectable()
class UsersService implements OnApplicationShutdown {
  onApplicationShutdown(signal: string) {
    console.log(signal); // e.g., "SIGINT"
  }
}
```

This feature is often used with Kubernetes to manage container lifecycles, with Heroku dynos, and with similar services.

Gotchas:
- `app.close()` runs the shutdown sequence and closes the server but does not terminate the Node process; active intervals or long-running tasks keep it alive.
- On Windows, `SIGINT` works, as do `SIGBREAK` and partly `SIGHUP`, but `SIGTERM` never works.
- Running several Nest apps in one process (parallel tests) with shutdown hooks enabled can trigger Node's "too many listeners" warning.

## Checked

2026-11-04. Read the whole lifecycle events page (`content/fundamentals/lifecycle-events.md` in nestjs/docs.nestjs.com). Confirmed shutdown hooks off by default, `enableShutdownHooks()`, hook order and signal parameters, Promise waiting, the Kubernetes and Heroku remark, the `app.close()` hint, the Windows signal warning and the too-many-listeners hint. Removed the Verify step (the page never ties Ctrl+C to a signal).
Method: documentation only; no commands were run.
