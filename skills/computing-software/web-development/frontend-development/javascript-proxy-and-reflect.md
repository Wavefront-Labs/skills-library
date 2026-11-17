---
id: computing-software.web-development.frontend-development.javascript-proxy-and-reflect
name: javascript-proxy-and-reflect
category: computing-software
field: web-development
product: frontend-development
tags: [javascript-classes, proxy-reflect, metaprogramming, javascript, reactivity]
level: practitioner
status: verified
description: "Using Proxy traps with Reflect forwarding for validation, observation and defaults; invariants, receiver handling, identity and performance pitfalls."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect
  - https://tc39.es/ecma262/#sec-proxy-object-internal-methods-and-internal-slots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxy and Reflect

## 1. Pattern: always forward with Reflect
```js
const cache = new WeakMap();                          // same target -> same proxy (keyed by target only)
const watched = (target, onChange) => {
  if (cache.has(target)) return cache.get(target);
  const p = new Proxy(target, {
    get(t, key, receiver) {
      const v = Reflect.get(t, key, receiver);           // receiver keeps getters' `this` correct
      return typeof v === "object" && v !== null ? watched(v, onChange) : v;
    },
    set(t, key, value, receiver) {
      const old = t[key];
      const ok = Reflect.set(t, key, value, receiver);
      if (ok && old !== value) onChange(key, value, old);
      return ok;                                           // must return boolean; false throws in strict mode
    },
    deleteProperty(t, key) { const ok = Reflect.deleteProperty(t, key); onChange(key, undefined); return ok; },
  });
  cache.set(target, p);
  return p;
};
```
`Reflect.*` mirrors each trap with the default behaviour and returns booleans instead of throwing.

## 2. Useful traps
`get`, `set`, `has` (`in`), `deleteProperty`, `ownKeys` (`Object.keys`, for-in), `getOwnPropertyDescriptor`, `defineProperty`, `apply`/`construct` (function proxies).

## 3. Use cases
- Validation: reject wrong types in `set` (throw `TypeError`).
- Defaults/missing-key detection: `get` returns fallback or throws on typos in config objects.
- Reactivity: Vue 3 `reactive()` and MobX are proxy-based.
- Revocable access: `Proxy.revocable(obj, handler)` then `revoke()` to cut off a capability.

## 4. Pitfalls
- **Invariants**: a trap cannot report a non-configurable, non-writable property differently from the target; violations throw `TypeError`.
- **Identity**: `proxy !== target`; Sets/Maps keyed by the raw object will not find the proxy. Cache proxies in a `WeakMap` so the same target yields the same proxy (without the cache `w.a === w.a` was `false` in a test; with the `WeakMap` above it is `true`).
- **Internal slots**: proxies of `Map`, `Set`, `Date`, DOM nodes, or classes with `#private` fields throw on method calls (`Method Map.prototype.get called on incompatible receiver`). Bind methods to the target in `get`, or avoid proxying these.
- **Performance**: every property access goes through the trap - keep proxies off hot loops.
- `JSON.stringify(proxy)` works (it goes through traps); `structuredClone(proxy)` throws.

Run in Node 20: `w.a.b = 2` fired `onChange` once, `Object.keys(w)` matched the target, `proxy.get` on a proxied `Map` threw `Method Map.prototype.get called on incompatible receiver`, a proxied class with `#x` threw on the getter, a `get` trap lying about a frozen property threw `TypeError`, a `set` trap returning `false` threw in strict mode, a revoked proxy threw `TypeError`, `JSON.stringify(proxy)` worked and `structuredClone(proxy)` threw `DataCloneError`.

## Verify
Unit tests for: nested set triggers onChange once; `Object.keys` matches target; same target returns same proxy.
