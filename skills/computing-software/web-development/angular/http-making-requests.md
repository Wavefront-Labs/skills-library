---
id: computing-software.web-development.angular.http-making-requests
name: http-making-requests
category: computing-software
field: web-development
product: angular
tags: [angular, http, httpclient, get, post, params, headers, responsetype, observe]
level: intro
status: docs-checked
description: "Make requests with Angular HttpClient: get and post, responseType, body serialization, HttpParams and HttpHeaders, observe response or events, progress and cold Observables."
sources:
  - https://angular.dev/guide/http/making-requests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`HttpClient` methods match HTTP verbs and return an RxJS `Observable` that sends the request on subscription. Each subscription makes a new backend request (cold Observables, like blueprints). Remember to `.subscribe()` mutation requests or nothing fires.

```ts
http.get<Config>('/api/config').subscribe((config) => { /* ... */ });
http.post<Config>('/api/config', newConfig).subscribe((config) => { /* ... */ });
```

The generic type is a type assertion; `HttpClient` does not verify the data matches. Without it the type is `Object`; consider `unknown` for uncertain data.

`responseType`: `'json'` (default), `'text'` (string), `'arraybuffer'`, `'blob'`. It must be a literal type: if options are extracted to a variable use `responseType: 'text' as const`. The same applies to `observe`.

Body serialization: string as plain text; number, boolean, array or plain object as JSON; `ArrayBuffer` as raw data; `Blob` as raw data with its content type; `FormData` as `multipart/form-data`; `HttpParams` or `URLSearchParams` as `application/x-www-form-urlencoded`.

URL params: `params: {filter: 'all'}` or an `HttpParams`, which is immutable (`set` and `append` return a new instance): `new HttpParams().set('filter', 'all').set('details', 'enabled')`. A custom encoder implements `HttpParameterCodec` (`encodeKey`, `encodeValue`, `decodeKey`, `decodeValue`) and is passed as `new HttpParams({encoder: new CustomHttpParamEncoder()})`; the default is `HttpUrlEncodingCodec`.

Headers: `headers: {'X-Debug-Level': 'verbose'}` or an immutable `HttpHeaders` (`new HttpHeaders().set(...)`).

`observe: 'response'` returns the whole response (`res.status`, `res.body`). `observe: 'events'` returns the event stream with `reportDownloadProgress: true` and/or `reportUploadProgress`; handle `HttpEventType.DownloadProgress` (`event.loaded`, `event.total`) and `HttpEventType.Response`. Other types: `Sent`, `UploadProgress`, `ResponseHeader`, `User` (custom event from an interceptor). Progress events are off by default because of cost. The default fetch backend does not support upload progress and throws if you set `reportUploadProgress`; use `withXhr()` for that.

Lifecycle: unsubscribing aborts an in-progress request (useful with the `async` pipe and `switchMap`). Responses usually complete, so leaks are unlikely, but clean up subscriptions on destroy; `async` pipe and `toSignal` do this.

Best practice: wrap requests in an injectable service (`getUser(id)` returning `this.http.get<User>(`/api/user/${id}`)`), and render with `@if (user$ | async; as user)`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/making-requests (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
