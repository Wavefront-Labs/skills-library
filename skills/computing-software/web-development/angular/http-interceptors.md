---
id: computing-software.web-development.angular.http-interceptors
name: http-interceptors
category: computing-software
field: web-development
product: angular
tags: [angular, http, interceptors, httprequest, httpcontext, withinterceptors, middleware]
level: practitioner
status: docs-checked
description: "Angular HttpClient interceptors: functional interceptors, request cloning, inject(), HttpContextToken metadata, synthetic responses, redirect and responseType info."
sources:
  - https://angular.dev/guide/http/interceptors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Interceptors are middleware for retrying, caching, logging, authentication and similar patterns. Functional interceptors are recommended over DI-based ones for more predictable behaviour.

```ts
export function loggingInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  console.log(req.url);
  return next(req);
}

bootstrapApplication(App, {
  providers: [provideHttpClient(withInterceptors([loggingInterceptor, cachingInterceptor]))],
});
```

They chain in the listed order (logging runs first, then forwards to caching).

Responses: transform the `Observable` of `HttpEvent`s from `next`; check `event.type === HttpEventType.Response` to find the final response:

```ts
return next(req).pipe(tap((event) => {
  if (event.type === HttpEventType.Response) console.log(req.url, 'returned', event.status);
}));
```

Modify requests by cloning, since `HttpRequest` and `HttpResponse` are immutable: `req.clone({headers: req.headers.set('X-New-Header', 'new header value')})`. This keeps interceptors idempotent when a request is resubmitted (such as a retry). The body is not protected from deep mutation, so take care if you mutate it.

Interceptors run in the injection context of the injector that registered them, so `inject` works:

```ts
export function authInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn) {
  const authToken = inject(AuthService).getAuthToken();
  return next(req.clone({headers: req.headers.append('X-Authentication-Token', authToken)}));
}
```

Metadata: `req.context` is an `HttpContext`, a typed map keyed by `HttpContextToken`. The default-value function gives each request its own object or array.

```ts
export const CACHING_ENABLED = new HttpContextToken<boolean>(() => true);
// in the interceptor: if (req.context.get(CACHING_ENABLED)) { ... }
http.get('/sensitive/data', {context: new HttpContext().set(CACHING_ENABLED, false)});
```

Unlike other request properties, the context is mutable, so a retried request shows earlier mutations.

Synthetic responses: an interceptor need not call `next`; it can build a response, e.g. from a cache, with `new HttpResponse({body: 'response body'})`.

With the fetch backend, responses carry `redirected` (check `event.redirected` and `event.url`) and `responseType`: `'basic'`, `'cors'`, `'opaque'` (limited headers and body), `'opaqueredirect'`, `'error'`.

DI-based: an `@Injectable()` class implementing `HttpInterceptor` (`intercept(req, handler)` returning `handler.handle(req)`), registered with `provideHttpClient(withInterceptorsFromDi())` plus `{provide: HTTP_INTERCEPTORS, useClass: LoggingInterceptor, multi: true}`. They run in provider registration order, which can be hard to predict in hierarchical DI.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/interceptors (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
