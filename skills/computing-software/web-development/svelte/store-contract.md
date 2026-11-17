---
id: computing-software.web-development.svelte.store-contract
name: store-contract
category: computing-software
field: web-development
product: svelte
tags: [store-contract, custom-store, subscribe-method, rxjs-interop, unsubscribe-function]
level: advanced
status: docs-checked
description: "The Svelte store contract: subscribe called synchronously with the current value, returning an unsubscribe, optional set, and RxJS observable interop caveats."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/06-runtime/01-stores.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
You can write stores without `svelte/store` by implementing the store contract:

```ts
store = { subscribe: (subscription: (value: any) => void) => (() => void), set?: (value: any) => void }
```

1. A store must have a `.subscribe` method that accepts a subscription function. That function must be called immediately and synchronously with the current value upon calling `.subscribe`. All active subscription functions must later be called synchronously whenever the value changes.
2. `.subscribe` must return an unsubscribe function. Calling it must stop that subscription, and the subscription function must not be called again.
3. A store may optionally have a `.set` method that accepts a new value and synchronously calls all active subscription functions. Such a store is a writable store.

RxJS interop: `.subscribe` may instead return an object with an `.unsubscribe` method. However, unless `.subscribe` synchronously calls the subscription (not required by the Observable spec), Svelte sees the store's value as `undefined` until it does.

Any object meeting the contract works with the `$store` prefix syntax in components (see `stores-basics`).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte stores page: the three-point store contract and RxJS interop caveat. Nothing removed.
