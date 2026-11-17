---
id: computing-software.web-development.angular.signals-writable-computed
name: signals-writable-computed
category: computing-software
field: web-development
product: angular
tags: [angular, signals, signal, computed, readonly, equality, issignal]
level: intro
status: docs-checked
description: "Angular signals fundamentals: writable signals, set and update, asReadonly, lazy memoized computed signals, equality functions and isSignal checks."
sources:
  - https://angular.dev/guide/signals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A signal wraps a value and notifies consumers when it changes. Read by calling it, which lets Angular track where it is used.

Writable signals (`WritableSignal`):

```ts
const count = signal(0);
console.log('The count is: ' + count());
count.set(3);
count.update((value) => value + 1);
```

`asReadonly()` returns a readonly view that reflects changes but cannot be `set` or `update`d. It has no built-in protection against deep mutation of its value.

```ts
private readonly _count = signal(0);
readonly count = this._count.asReadonly();
```

Computed signals are read-only and derive from other signals:

```ts
const count: WritableSignal<number> = signal(0);
const doubleCount: Signal<number> = computed(() => count() * 2);
```

- Lazy and memoized: the derivation does not run until first read, then the value is cached until a dependency changes. Expensive derivations such as filtering arrays are safe.
- Not writable: `doubleCount.set(3)` is a compile error.
- Dynamic dependencies: only signals actually read in the latest run are tracked. In `computed(() => showCount() ? `The count is ${count()}.` : 'Nothing to see here!')`, `count` is not a dependency while `showCount()` is false, and dependencies can be removed as well as added.

Equality: pass `{equal: fn}` to writable or computed signals to decide whether a new value really differs. The default is referential equality (`Object.is()`).

```ts
const data = signal(['test'], {equal: isEqual}); // lodash isEqual
data.set(['test']); // considered equal, no updates
```

Type checks: `isSignal(count)` is true for any signal (and `computed`), false for `42`; `isWritableSignal(count)` is true only for writable ones.

Reading signals inside an `OnPush` component template marks the component for check when the signal changes.

## Checked

Method: 2026-11-08 compared against the Angular signals guide source markdown (adev guide signals/overview). Writable, readonly, computed, equality and type-check claims match the page. Dropped a cross-reference to another skill id that the page does not state.
