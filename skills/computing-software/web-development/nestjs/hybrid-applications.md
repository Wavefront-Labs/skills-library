---
id: computing-software.web-development.nestjs.hybrid-applications
name: hybrid-applications
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, hybrid, microservices, connectmicroservice, transport]
level: advanced
status: docs-checked
description: "Combine an HTTP server with one or more microservice listeners in NestJS using connectMicroservice, startAllMicroservices and inheritAppConfig."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/hybrid-application.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A hybrid app listens on several sources. `createMicroservice()` supports only one server, so attach microservices to an HTTP app:

```typescript
const app = await NestFactory.create(AppModule);
const microservice = app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.TCP,
});

await app.startAllMicroservices();
await app.listen(3001);
```

If the app serves no HTTP, call `app.init()` instead of `app.listen()`. Call `connectMicroservice()` once per transport (for example TCP on port 3002 and Redis on `localhost:6379`).

Bind a handler to a single transport by passing a second argument to `@MessagePattern()`:

```typescript
@MessagePattern('time.us.*', Transport.NATS)
getDate(@Payload() data: number[], @Ctx() context: NatsContext) {}

@MessagePattern({ cmd: 'time.us' }, Transport.TCP)
getTCPDate(@Payload() data: number[]) {}
```

For a custom transporter use the `transportId` symbol of its server class.

Sharing global config: connected microservices do not inherit global pipes, interceptors, guards and filters (neither `useGlobal*()` nor `APP_*` tokens). Opt in:

```typescript
app.connectMicroservice<MicroserviceOptions>(
  { transport: Transport.TCP },
  { inheritAppConfig: true },
);
```

Gotchas:
- Order matters. `startAllMicroservices()` before `listen()` lets microservices consume messages before `onModuleInit` and `onApplicationBootstrap` have completed. Call `listen()` or `init()` first if handlers must wait for full initialization.
- With `inheritAppConfig`, call `useGlobalPipes()`, `useGlobalGuards()` and the others before `connectMicroservice()`, since handlers are registered at that call.

## Checked

2026-11-04. Read the whole hybrid application page (`content/faq/hybrid-application.md` in nestjs/docs.nestjs.com). Confirmed `connectMicroservice()`, `startAllMicroservices()`, the `app.init()` hint, the call-order notice, multiple transports, `@MessagePattern()` with a transport argument and `transportId`, and `inheritAppConfig` with its call-order hint. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
