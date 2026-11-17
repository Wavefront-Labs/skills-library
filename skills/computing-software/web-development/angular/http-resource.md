---
id: computing-software.web-development.angular.http-resource
name: http-resource
category: computing-software
field: web-development
product: angular
tags: [angular, http, httpresource, signals, parse, zod, progress]
level: practitioner
status: docs-checked
description: "Reactive Angular data fetching with httpResource: URL and request objects, response type helpers, download progress, parse validation and unit testing."
sources:
  - https://angular.dev/guide/http/http-resource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`httpResource` is a reactive wrapper around `HttpClient` exposing request status and response as signals, so it works with `computed`, `effect` and `linkedSignal`. It supports the same features as `HttpClient`, such as interceptors, and uses the globally available `HttpClient`; call `provideHttpClient(...)` only to configure features.

```ts
userId = input.required<string>();
user = httpResource(() => `/api/user/${userId()}`);
```

When a dependent signal changes it issues a new request, cancelling an outstanding one. Unlike `HttpClient`, which starts requests on subscription, it initiates requests eagerly.

For richer requests return an object; each reactive property should come from a signal:

```ts
user = httpResource(() => ({
  url: `/api/user/${userId()}`,
  method: 'GET',
  headers: {'X-Special': 'true'},
  params: {'fast': 'yes'},
  reportProgress: true,
  transferCache: true,
  keepalive: true,
  priority: 'high',
  credentials: 'include',
}));
```

Avoid `httpResource` for mutations like POST or PUT; use `HttpClient` directly.

Template use. Reading `value` in the error state throws, so guard with `hasValue()`:

```angular-html
@if (user.hasValue()) {
  <user-details [user]="user.value()" />
} @else if (user.error()) {
  <div>Could not load user information</div>
} @else if (user.isLoading()) {
  <div>Loading user info...</div>
}
```

Response types (default is JSON): `httpResource.text(...)` gives a string, `httpResource.blob(...)` a `Blob`, `httpResource.arrayBuffer(...)` an `ArrayBuffer`.

Progress: `reportProgress: true` exposes the latest `HttpProgressEvent` on the `progress` signal: `downloaded = computed(() => this.file.progress()?.loaded ?? 0);`. Unlike `HttpClient`, it keeps one `reportProgress` option, and it only enables download progress.

Validation: the `parse` option (for example Zod's `schema.parse`) validates responses; its return type becomes the type of `value`:

```ts
swPersonResource = httpResource(() => `https://swapi.info/api/people/${this.id()}`, {
  parse: starWarsPersonSchema.parse,
});
```

Testing uses the same APIs as `HttpClient`:

```ts
TestBed.configureTestingModule({providers: [provideHttpClientTesting()]});
const id = signal(0);
const mockBackend = TestBed.inject(HttpTestingController);
const response = httpResource(() => `/data/${id()}`, {injector: TestBed.inject(Injector)});
TestBed.tick(); // triggers the effect
mockBackend.expectOne('/data/0').flush(0);
await TestBed.inject(ApplicationRef).whenStable();
expect(response.value()).toEqual(0);
```

Underlying pattern: `computing-software.web-development.angular.resource-api`.

## Checked

Date: 2026-11-07

Read in full: https://angular.dev/guide/http/http-resource (source Markdown from the angular/angular repository, adev/src/content/guide, plus the live page text where the fetch returned content). Inline code snippets were read; no separate example files were opened.
No corrections needed; every claim was confirmed against the page.

Method: documentation only; no commands were run.
