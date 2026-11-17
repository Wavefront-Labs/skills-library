---
id: computing-software.web-development.nestjs.interceptor-errors-timeout-cache
name: interceptor-errors-timeout-cache
category: computing-software
field: web-development
product: nestjs
tags: [nestjs, interceptors, rxjs, timeout, caching]
level: advanced
status: docs-checked
description: "Use NestJS interceptors with catchError, timeout and of() to remap exceptions, enforce request timeouts and short-circuit handlers with cached results."
sources:
  - https://github.com/nestjs/docs.nestjs.com/blob/master/content/interceptors.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Because `next.handle()` returns an Observable, RxJS operators can change errors and even skip the handler.

Exception mapping:

```typescript
return next.handle().pipe(
  catchError(err => throwError(() => new BadGatewayException())),
);
```

Timeout:

```typescript
@Injectable()
export class TimeoutInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      timeout(5000),
      catchError(err => {
        if (err instanceof TimeoutError) {
          return throwError(() => new RequestTimeoutException());
        }
        return throwError(() => err);
      }),
    );
  }
}
```

`timeout`, `catchError` come from `rxjs/operators`; `throwError`, `TimeoutError`, `of` from `rxjs`.

Stream overriding (skip the handler):

```typescript
intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
  const isCached = true;
  if (isCached) {
    return of([]);   // handler is NOT called
  }
  return next.handle();
}
```

The docs' sample hardcodes the cache flag and response. A real one needs TTL, invalidation and size limits; for a generic solution, use `Reflector` together with a custom decorator, as described in the guards chapter.

Bind the same way as any interceptor (`@UseInterceptors(TimeoutInterceptor)`).

Gotchas:
- `timeout()` only fails the stream. Unsubscribing does not abort work the handler already started (like a pending DB query), so add resource-release logic before throwing `RequestTimeoutException`.
- `tap()` is not called when the handler throws; use `catchError` (as in the samples above), an observer with an `error` callback, or `finalize()` for failure paths.

Verify: add a handler that does not respond within 5 seconds and confirm the response is a `RequestTimeoutException`. With the cache sample bound, the endpoint returns the hardcoded `[]` and the handler body is never called.

## Checked

2026-11-04. Read the whole interceptors page (`content/interceptors.md` in nestjs/docs.nestjs.com). Confirmed exception mapping with `catchError()`, stream overriding with `of()`, the hardcoded-cache caveat and `Reflector` pointer, the timeout interceptor, the note that unsubscribing does not abort started work, and the `tap()` error note. Nothing removed. The Verify steps are kept because the page states both outcomes (a `TimeoutError` becomes `RequestTimeoutException`; the cache sample returns `[]` without calling the handler).
Method: documentation only; no commands were run.
