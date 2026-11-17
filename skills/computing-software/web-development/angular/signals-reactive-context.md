---
id: computing-software.web-development.angular.signals-reactive-context
name: signals-reactive-context
category: computing-software
field: web-development
product: angular
tags: [angular, signals, reactive-context, untracked, async, assertnotinreactivecontext]
level: advanced
status: docs-checked
description: "Angular reactive contexts: where signal reads are tracked, untracked reads, assertNotInReactiveContext, and losing tracking after an await."
sources:
  - https://angular.dev/guide/signals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A reactive context is a runtime state where Angular monitors signal reads to establish dependencies. The code reading is the consumer; the signal read is the producer. Angular enters a reactive context automatically when:
- executing an `effect` or `afterRenderEffect` callback,
- evaluating a `computed` signal,
- evaluating a `linkedSignal`,
- evaluating a `resource`'s params function,
- rendering a component template (including bindings in the host property).

If a tracked signal changes, Angular will eventually re-run the consumer.

Assert you are not in one with `assertNotInReactiveContext`, passing the calling function so the error points to the right API:

```ts
function subscribeToEvents() {
  assertNotInReactiveContext(subscribeToEvents);
}
```

Reading without tracking: wrap a read in `untracked` so it does not become a dependency.

```ts
effect(() => {
  console.log(`User set to ${currentUser()} and the counter is ${untracked(counter)}`);
});

effect(() => {
  const user = currentUser();
  untracked(() => {
    // signals read by the service are not dependencies of this effect
    this.loggingService.log(`User set to ${user}`);
  });
});
```

Async: the reactive context is only active for synchronous code. Signal reads after an asynchronous boundary are not tracked.

```ts
// avoid: theme() is read after the await and is not tracked
effect(async () => {
  const data = await fetchUserData();
  console.log(`User: ${data.name}, Theme: ${theme()}`);
});

// prefer: read before the await
effect(async () => {
  const currentTheme = theme();
  const data = await fetchUserData();
  console.log(`User: ${data.name}, Theme: ${currentTheme}`);
});
```

Arguments passed to the awaited function are evaluated synchronously, so `await renderContent(docContent());` also tracks `docContent`.

## Checked

Method: 2026-11-08 compared against the Angular signals guide source markdown (adev guide signals/overview), Reactive contexts section. List of contexts, assertNotInReactiveContext, untracked and the async rules match the page. Dropped cross-references to other skill ids that the page does not state.
