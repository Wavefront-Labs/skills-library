---
id: computing-software.web-development.nestjs.custom-exception-filters
name: custom-exception-filters
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, exception-filters, catch, error-handling, arguments-host]
level: practitioner
status: docs-checked
description: "Create and bind a NestJS ExceptionFilter with Catch and ArgumentsHost to shape error responses, at method, controller or global scope, including middleware errors."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/exception-filters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Implement `ExceptionFilter<T>` with `catch(exception: T, host: ArgumentsHost)` and mark it with `@Catch(...)`, which takes one or a comma-separated list of exception types.

```typescript
@Catch(HttpException)
export class HttpExceptionFilter implements ExceptionFilter {
  catch(exception: HttpException, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const status = exception.getStatus();
    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
    });
  }
}
```

With `@nestjs/platform-fastify`, use `response.send()` instead of `json()` and fastify types.

Binding:

```typescript
@Post()
@UseFilters(HttpExceptionFilter)      // class preferred: instances are reused, DI works
async create(@Body() dto: CreateCatDto) { throw new ForbiddenException(); }
```

Controller scope: `@UseFilters(...)` on the class. Global: `app.useGlobalFilters(new HttpExceptionFilter())` (no DI, and not applied to gateways or hybrid apps) or `{ provide: APP_FILTER, useClass: HttpExceptionFilter }` from any module. Register as many `APP_FILTER` providers as needed.

Exceptions thrown from middleware also reach the exceptions layer, but only global filters apply because no route handler is chosen yet; `@UseFilters()` bindings are not invoked.

Gotcha: filters are the way to log built-in HTTP exceptions, since the default filter does not log them. A filter decides what the client sees; on its own it does not record or group errors. Prefer binding by class rather than by instance, which reduces memory usage because Nest can reuse instances of the same class across the module.

## Checked

2026-11-04. Read the whole exception filters page (`content/exception-filters.md` in nestjs/docs.nestjs.com). Confirmed `ExceptionFilter<T>`, `@Catch` list form, the example body, the Fastify `send()` note, `@UseFilters` by class or instance, method/controller/global scope, `useGlobalFilters` limits, `APP_FILTER`, the middleware hint, built-in filters not logging `HttpException`, and the class-over-instance memory hint. Removed the Verify step (not on the page).
Method: documentation only; no commands were run.
