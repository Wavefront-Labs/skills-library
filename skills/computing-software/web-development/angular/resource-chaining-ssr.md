---
id: computing-software.web-development.angular.resource-chaining-ssr
name: resource-chaining-ssr
category: computing-software
field: web-development
product: angular
tags: [angular, signals, resource, chain, transferstate, ssr, snapshot, resourcefromsnapshots]
level: advanced
status: docs-checked
description: "Chain dependent resources, cache resource results from SSR with an id, and compose resources with ResourceSnapshot and resourceFromSnapshots."
sources:
  - https://angular.dev/guide/signals/resource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
SSR caching: a resource loader runs once on the server and the browser normally runs it again at hydration. Provide an `id` to store the resolved value in `TransferState` and initialize the client resource as `'resolved'`:

```ts
const userResource = resource({
  params: () => ({id: userId()}),
  loader: ({params}) => fetchUser(params),
  id: 'user-unique-id',
});
```

The `id` must be unique in the app and identical on server and client. The value is serialized into the page HTML, so avoid `id` on resources loading data specific to the user who triggered the render, especially if the HTML can be cached or shared.

Chaining: express a dependency with `chain` from the `params` context.

```ts
const companyResource = resource({
  params: ({chain}) => chain(userResource)?.companyId,
  loader: ({params: companyId}) => fetchCompany(companyId),
});
```

`chain(userResource)` propagates status:
- upstream idle: downstream idle.
- loading or reloading: downstream enters `loading` and its loader does not run (during `reloading`, `chain` does not return the previous value).
- error: downstream enters `error`.
- resolved or local: `chain` returns the current value, which may itself be `undefined`, making params `undefined` and the downstream idle.

Pass the chained value directly as params, not wrapped in an object: `{companyId: undefined}` is a defined value so the loader would run with an undefined id. Reading `userResource.value()` directly inside params works but just goes `idle` rather than mirroring `loading` and `error`; prefer `chain`. Use `chain` only when the downstream does its own async work; for a synchronous derived value use `computed`.

Snapshots: every resource has a `snapshot` signal holding a `status` and either a `value` or an `error`. `resourceFromSnapshots` (experimental, may change) builds a resource from a snapshot signal, enabling composition with `computed` and `linkedSignal`:

```ts
function withPreviousValue<T>(input: Resource<T>): Resource<T> {
  const derived = linkedSignal<ResourceSnapshot<T>, ResourceSnapshot<T>>({
    source: input.snapshot,
    computation: (snap, previous) => {
      if (snap.status === 'loading' && previous && previous.value.status !== 'error') {
        return {status: 'loading' as const, value: previous.value.value};
      }
      return snap;
    },
  });
  return resourceFromSnapshots(derived);
}
```

Used as `user = withPreviousValue(httpResource(() => `/user/${this.userId()}`))`, the old user data stays until the new one loads.

## Checked

Method: 2026-11-08 compared against the Angular resource guide source markdown (adev guide signals/resource), sections on SSR caching, chaining and snapshots. All claims match the page; no changes to the technical content.
