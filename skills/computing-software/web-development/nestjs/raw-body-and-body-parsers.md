---
id: computing-software.web-development.nestjs.raw-body-and-body-parsers
name: raw-body-and-body-parsers
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, raw-body, body-parser, webhooks, express]
level: practitioner
status: docs-checked
description: "Access the raw request body for webhook signature checks in NestJS Express or Fastify, register extra body parsers, and raise size limits."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/faq/raw-body.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Webhook signature verification usually needs the unparsed body to compute an HMAC. Enable `rawBody` when creating the app (works only if the built-in body parser is on, so do not pass `bodyParser: false`).

Express:

```typescript
const app = await NestFactory.create<NestExpressApplication>(AppModule, {
  rawBody: true,
});

@Post()
create(@Req() req: RawBodyRequest<Request>) {
  const raw = req.rawBody; // a Buffer
}
```

Fastify:

```typescript
const app = await NestFactory.create<NestFastifyApplication>(
  AppModule,
  new FastifyAdapter(),
  { rawBody: true },
);
// controller: @Req() req: RawBodyRequest<FastifyRequest>
```

`RawBodyRequest` is exported from `@nestjs/common`.

Additional parsers: only `json` and `urlencoded` (Fastify: `application/json` and `application/x-www-form-urlencoded`) are registered by default.

```typescript
app.useBodyParser('text');                 // Express
app.useBodyParser('text/plain');           // Fastify
```

Size limits (Express default 100kb, Fastify default 1 MiB):

```typescript
app.useBodyParser('json', { limit: '10mb' });                         // Express
app.useBodyParser('application/json', { bodyLimit: 10_485_760 });     // Fastify
```

`useBodyParser()` respects the `rawBody` option.

Gotcha: type the app correctly (`NestExpressApplication` or `NestFastifyApplication`), otherwise `useBodyParser()` is not found.

## Checked

2026-11-04. Confirmed against the official NestJS docs source: rawBody option, RawBodyRequest, useBodyParser, default limits, Express and Fastify forms (raw-body page). Removed: invented Verify step.

Method: documentation only; no commands were run.
