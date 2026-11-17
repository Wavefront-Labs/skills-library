---
id: computing-software.web-development.angular.resource-api
name: resource-api
category: computing-software
field: web-development
product: angular
tags: [angular, signals, resource, loader, abortsignal, resource-status, stream, reload]
level: practitioner
status: docs-checked
description: "Angular resource(): params and loader, abort signals, reload, streaming sources, and the status, value, hasValue, error and isLoading signals."
sources:
  - https://angular.dev/guide/signals/resource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `Resource` brings async data into signal code while letting you read it synchronously. Create one with `resource`:

```ts
const userId: Signal<string> = getUserId();

const userResource = resource({
  params: () => ({id: userId()}),          // reactive; recomputes when read signals change
  loader: ({params}) => fetchUser(params), // called every time params changes
});

const firstName = computed(() => {
  if (userResource.hasValue()) {
    return userResource.value().firstName;
  }
  return undefined;
});
```

`hasValue` is both a type guard that strips `undefined` and protection against reading a throwing `value` in the error state.

Loader parameters (`ResourceLoaderParams`): `params`, `previous` (an object with the previous `status`) and `abortSignal`. If `params` returns `undefined`, the loader does not run and the status is `'idle'`.

Aborting: a resource aborts an outstanding load if `params` changes while loading. Pass the signal on: `loader: ({params, abortSignal}) => fetch(`users/${params.id}`, {signal: abortSignal}).then((res) => res.json())`.

Reloading: call `userResource.reload()`.

Streaming: for sources producing many values (WebSockets, SSE, Firestore `onSnapshot`) use `stream` instead of `loader`; its signal keeps updating. Use `loader` for one-time operations like an HTTP fetch.

```ts
const userUpdates = signal({value: 'Alice'});
const userResource = resource({ stream: () => userUpdates });
userUpdates.set({value: 'Bob'});
```

Status signals: `value` (most recent, or `defaultValue`, else `undefined`; throws when status is `'error'`), `hasValue`, `error`, `isLoading`, `status`.

| Status | value() |
| --- | --- |
| idle | undefined |
| error | throws |
| loading | undefined |
| reloading | previous value |
| resolved | resolved value |
| local | locally set value via `.set()` or `.update()` |

Use these for loading indicators and error messages. `httpResource` wraps `HttpClient` for HTTP, going through the Angular HTTP stack including interceptors.

## Checked

Method: 2026-11-08 compared against the Angular resource guide source markdown (adev guide signals/resource). Loader parameters, abort, reload, stream, status table and httpResource note match the page. Dropped two cross-reference sentences to other skill ids that the page does not state.
