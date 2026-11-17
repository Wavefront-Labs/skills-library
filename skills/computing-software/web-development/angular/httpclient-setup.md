---
id: computing-software.web-development.angular.httpclient-setup
name: httpclient-setup
category: computing-software
field: web-development
product: angular
tags: [angular, http, httpclient, providehttpclient, withxhr, withinterceptors, xsrf, jsonp]
level: intro
status: docs-checked
description: "Set up Angular HttpClient with provideHttpClient and its features: withXhr, withInterceptors, withInterceptorsFromDi, withRequestsMadeViaParent, XSRF, and module equivalents."
sources:
  - https://angular.dev/guide/http/setup
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`HttpClient` is available for injection by default in Angular v21 and later. Use `provideHttpClient` in `app.config.ts` to configure the default feature set or add features:

```ts
export const appConfig: ApplicationConfig = {
  providers: [provideHttpClient(/* features such as withInterceptors(...) */)],
};
```

NgModule apps put `provideHttpClient(...)` in the module's `providers`. Then `private http = inject(HttpClient);`.

Features:
- `withXhr()`: by default `HttpClient` uses the `fetch` API; this switches to `XMLHttpRequest`. `fetch` has limitations such as not producing upload progress events. Do not use `withXhr` in SSR: XHR support on the server is deprecated and intended to be removed in Angular 23, because the underlying `xhr2` library does not safely handle redirects (it can forward `Authorization` headers on cross-origin redirects and is susceptible to DoS via redirect loops). Use the default `fetch` backend for SSR.
- `withInterceptors([...])`: functional interceptors. See `computing-software.web-development.angular.http-interceptors`.
- `withInterceptorsFromDi()`: includes older class-based interceptors. Functional interceptors have more predictable ordering and are recommended.
- `withRequestsMadeViaParent()`: by default `provideHttpClient` in an injector overrides the parent injector's configuration. With this feature, requests pass up to the parent `HttpClient` after this level's interceptors, so you can add interceptors in a child injector while keeping the parent's. An `HttpClient` must be configured above the current injector or you get a runtime error.
- `withJsonpSupport()`: enables `.jsonp()`. Deprecated, as are `HttpClientJsonpModule` and `.jsonp()`, because JSONP can cause XSS vulnerabilities; use CORS.
- `withXsrfConfiguration(...)` customises built-in XSRF protection; `withNoXsrfProtection()` disables it.

Deprecated NgModule equivalents:

| NgModule | Equivalent |
| --- | --- |
| `HttpClientModule` | `provideHttpClient(withInterceptorsFromDi(), withXhr())` |
| `HttpClientJsonpModule` | `withJsonpSupport()` |
| `HttpClientXsrfModule.withOptions(...)` | `withXsrfConfiguration(...)` |
| `HttpClientXsrfModule.disable()` | `withNoXsrfProtection()` |

With `HttpClientModule` present in multiple injectors, interceptor behaviour is poorly defined and depends on options and ordering; prefer `provideHttpClient`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/setup (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
