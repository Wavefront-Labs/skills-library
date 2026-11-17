---
id: computing-software.web-development.angular.http-testing
name: http-testing
category: computing-software
field: web-development
product: angular
tags: [angular, http, testing, httptestingcontroller, providehttpclienttesting, flush, interceptors]
level: practitioner
status: docs-checked
description: "Test Angular HttpClient code with provideHttpClientTesting and HttpTestingController: expectOne, flush, match, expectNone, verify, error simulation and interceptors."
sources:
  - https://angular.dev/guide/http/testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Mock the HTTP backend. The app makes requests first; the test expects requests, asserts on them, then "flushes" responses, and finally verifies no unexpected requests occurred.

Setup: include `provideHttpClientTesting()` in `TestBed`; it switches `HttpClient` to a test backend and provides `HttpTestingController`.

```ts
TestBed.configureTestingModule({providers: [provideHttpClientTesting()]});
const httpTesting = TestBed.inject(HttpTestingController);
```

To configure `HttpClient` features such as interceptors, put `provideHttpClient(...)` before `provideHttpClientTesting()`, because the latter overwrites parts of the former:

```ts
providers: [provideHttpClient(withInterceptors([authInterceptor])), provideHttpClientTesting()]
```

Expect and answer:

```ts
const configPromise = firstValueFrom(service.getConfig<Config>());
const req = httpTesting.expectOne('/api/config', 'Request to load the configuration');
expect(req.request.method).toBe('GET');
req.flush(DEFAULT_CONFIG);
expect(await configPromise).toEqual(DEFAULT_CONFIG);
httpTesting.verify();
```

`expectOne` fails if more than one request matches. Match method too with `expectOne({method: 'GET', url: '/api/config'}, 'description')`. Matching uses the full URL including query parameters. Move `verify()` into `afterEach()`.

Multiple requests: `httpTesting.match({method: 'GET'})` returns an array; matched requests are removed from future matching and you must flush and verify them. All matchers accept a predicate: `httpTesting.expectOne((req) => req.body !== null)`. `expectNone` asserts nothing matches: `httpTesting.expectNone((req) => req.method !== 'GET')`.

Errors:

```ts
req.flush('Failed!', {status: 500, statusText: 'Internal Server Error'}); // backend error
req.error(new ProgressEvent('network error!'));                            // network error
```

Interceptors: test one at a time with `provideHttpClient(withInterceptors([authInterceptor]))`, make a request through `HttpClient`, then inspect `httpTesting.expectOne('/api/config').request.headers.get('X-Authentication-Token')`. For class-based interceptors use `provideHttpClient(withInterceptorsFromDi())` and `{provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true}`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/testing (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
