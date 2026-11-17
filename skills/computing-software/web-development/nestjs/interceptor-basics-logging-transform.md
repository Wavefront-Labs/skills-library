---
id: computing-software.web-development.nestjs.interceptor-basics-logging-transform
name: interceptor-basics-logging-transform
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, interceptors, rxjs, aop, response-mapping]
level: practitioner
status: docs-checked
description: "Write NestJS interceptors with intercept and CallHandler.handle to run code before and after handlers and to map responses with RxJS map and tap."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/interceptors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
An interceptor is an `@Injectable()` class implementing `NestInterceptor` with `intercept(context: ExecutionContext, next: CallHandler)`. It wraps the request/response stream: code before `next.handle()` runs pre-handler; operators on the returned Observable run post-handler. If you never call `handle()`, the route handler does not run.

```typescript
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    console.log('Before...');
    const now = Date.now();
    return next.handle().pipe(
      tap(() => console.log(`After... ${Date.now() - now}ms`)),
    );
  }
}
```

Response mapping with `map()`:

```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
    return next.handle().pipe(map(data => ({ data })));
  }
}
```

A handler returning `[]` now responds `{ "data": [] }`. Another global example is `map(value => value === null ? '' : value)`.

Binding: `@UseInterceptors(LoggingInterceptor)` at controller or method level (class or instance), `app.useGlobalInterceptors(new LoggingInterceptor())`, or with DI `{ provide: APP_INTERCEPTOR, useClass: LoggingInterceptor }`. `intercept()` may be `async`. Interceptors can inject constructor dependencies.

Gotchas:
- `tap()` does not run when the handler throws; use an observer with an `error` callback or `finalize()`.
- Response mapping does not work with the library-specific strategy (`@Res()` sending the response itself); use `@Res({ passthrough: true })`.

Verify: hit `GET /cats` and check the "Before..." and "After... Nms" lines, and that the JSON body is wrapped in `data`.

## Checked

2026-11-04. Read the whole interceptors page (`content/interceptors.md` in nestjs/docs.nestjs.com). Confirmed `NestInterceptor`, `CallHandler.handle()`, the before and after behaviour, `LoggingInterceptor` and its console output, `TransformInterceptor` and its `{ "data": [] }` result, the null-to-empty-string example, binding forms, `async` `intercept()`, DI in interceptors, the `tap()` error note and the `@Res()` passthrough warning. Nothing removed. The Verify step is kept because the page shows the log output and the wrapped body for `GET /cats`.
Method: documentation only; no commands were run.
