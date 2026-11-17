---
id: computing-software.web-development.nestjs.catch-all-and-base-exception-filter
name: catch-all-and-base-exception-filter
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, exception-filters, httpadapterhost, baseexceptionfilter, fastify]
level: advanced
status: docs-checked
description: "Catch every exception in NestJS with a platform-agnostic filter using HttpAdapterHost, or extend BaseExceptionFilter to delegate to the built-in handling."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/exception-filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An empty `@Catch()` catches all unhandled exceptions. To stay platform-agnostic (Express and Fastify) deliver the response through the HTTP adapter:

```typescript
@Catch()
export class CatchEverythingFilter implements ExceptionFilter {
  constructor(private readonly httpAdapterHost: HttpAdapterHost) {}

  catch(exception: unknown, host: ArgumentsHost): void {
    // httpAdapter may not exist in the constructor in some situations
    const { httpAdapter } = this.httpAdapterHost;
    const ctx = host.switchToHttp();
    const httpStatus =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;
    const responseBody = {
      statusCode: httpStatus,
      timestamp: new Date().toISOString(),
      path: httpAdapter.getRequestUrl(ctx.getRequest()),
    };
    httpAdapter.reply(ctx.getResponse(), responseBody, httpStatus);
  }
}
```

Register it with `{ provide: APP_FILTER, useClass: CatchEverythingFilter }`.

If you combine a catch-everything filter with one bound to a specific exception type, declare the catch-everything filter first so the specific filter can still handle its type.

To keep default behavior in some cases, extend `BaseExceptionFilter` (from `@nestjs/core`) and call `super.catch(exception, host)`:

```typescript
@Catch()
export class AllExceptionsFilter extends BaseExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    super.catch(exception, host);
  }
}
```

Global registration without a module:

```typescript
const { httpAdapter } = app.get(HttpAdapterHost);
app.useGlobalFilters(new AllExceptionsFilter(httpAdapter));
```

or use the `APP_FILTER` token.

Gotcha: method-scoped and controller-scoped filters extending `BaseExceptionFilter` must not be created with `new`; let the framework instantiate them.

## Checked

2026-11-04. Read the whole exception filters page (`content/exception-filters.md` in nestjs/docs.nestjs.com). Confirmed the empty `@Catch()` filter, `HttpAdapterHost` and `httpAdapter.reply`/`getRequestUrl`, the catch-everything-first warning, `BaseExceptionFilter` from `@nestjs/core`, the two global registration routes and the do-not-use-`new` warning. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
