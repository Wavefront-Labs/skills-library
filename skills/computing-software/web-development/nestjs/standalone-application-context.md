---
id: computing-software.web-development.nestjs.standalone-application-context
name: standalone-application-context
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, standalone, createapplicationcontext, cron, cli]
level: practitioner
status: docs-checked
description: "Run NestJS without an HTTP server using createApplicationContext to call providers from scripts, CRON jobs or CLIs, with get, select and close."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/application-context.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A standalone application wraps the IoC container with no network listeners. Use it for scripts, workers, CRON jobs and CLIs.

```typescript
async function bootstrap() {
  const app = await NestFactory.createApplicationContext(AppModule);
  const tasksService = app.get(TasksService);
  // ... application logic
  await app.close();
}
await bootstrap();
```

`app.get()` queries every registered module for the token. For strict checks navigate to a module with `select()`:

```typescript
const tasksService = app.select(TasksModule).get(TasksService, { strict: true });
```

In non-strict mode the root module is selected by default. For dynamic modules, pass `select()` the exact object that was imported:

```typescript
export const dynamicConfigModule = ConfigModule.register({ folder: './config' });
@Module({ imports: [dynamicConfigModule] })
export class AppModule {}

const configService = app.select(dynamicConfigModule).get(ConfigService, { strict: true });
```

Call `await app.close()` at the end so the Node.js process exits and shutdown lifecycle hooks run.

Gotcha: there is no request handling, so middleware, interceptors, pipes and guards are not available. Even a registered global interceptor will not execute when you call a retrieved controller's methods.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: createApplicationContext, get, select with strict, dynamic module selection, close and shutdown hooks (application-context page). Removed: NestFactory.create() advice (not on the page); invented Verify step.

Method: documentation only; no commands were run.
