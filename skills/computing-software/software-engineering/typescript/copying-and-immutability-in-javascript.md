---
id: computing-software.software-engineering.typescript.copying-and-immutability-in-javascript
name: copying-and-immutability-in-javascript
category: computing-software
field: software-engineering
product: typescript
tags: [javascript, structuredclone, object-freeze, shallow-copy, immutable-updates, change-array-by-copy, readonly]
level: practitioner
status: verified
description: "Copy and update data safely in JS: shallow spread vs structuredClone deep copies, immutable update patterns, toSorted/with array methods, Object.freeze limits and TS readonly."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Window/structuredClone", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying and immutability in JavaScript

**Goal:** no accidental shared-mutation bugs (state updates that don't re-render,
caches corrupted by callers).

## Shallow copies
```js
const copy = { ...user };                 // or Object.assign({}, user)
const arr2 = [...arr];                    // or arr.slice()
copy.address.city = "Paris";              // ALSO changes user.address: nested objects are shared
```

## Deep copies
```js
const deep = structuredClone(state);      // Node 17+ (Node docs); browsers: see the MDN compatibility table
```
Handles Dates, Maps, Sets, typed arrays, cycles. Throws DataCloneError on functions (run), and class
instances lose their prototype (become plain objects). `JSON.parse(JSON.stringify(x))` drops
`undefined`, functions and Dates (become strings) - avoid.

## Immutable update patterns
```js
const next = {
  ...state,
  user: { ...state.user, address: { ...state.user.address, city: "Paris" } },
  items: state.items.map((it) => (it.id === id ? { ...it, qty: it.qty + 1 } : it)),
  tags: state.tags.filter((t) => t !== "old"),
};
```
For deep updates, Immer (`produce(state, draft => { draft.user.address.city = "Paris" })`)
writes like mutation and returns structurally shared copies.

## Non-mutating array methods (ES2023)
`toSorted()`, `toReversed()`, `toSpliced()`, `with(index, value)` return new arrays.
`sort()`, `reverse()`, `splice()` mutate in place - `props.items.sort()` in React mutates props.

## Freezing
```js
const CONFIG = Object.freeze({ retries: 3, endpoints: { api: "/api" } });
CONFIG.retries = 5;          // silently ignored (TypeError in strict mode/ES modules)
CONFIG.endpoints.api = "x";  // works: freeze is shallow
```
Deep freeze needs recursion. Freezing costs little but isn't free in hot paths; mostly useful
for shared constants and dev-mode guards.

## TypeScript readonly (compile time only)
```ts
type State = Readonly<{ items: readonly Item[]; user: Readonly<User> }>;
function total(items: readonly Item[]) { ... }    // callers know you won't mutate
const ROUTES = { home: "/" } as const;             // deep readonly literal
```
Readonly types disappear at runtime; combine with immutable update habits.

## Verify
- [ ] No in-place `sort/reverse/splice` on props, state or function parameters (code review
      or a lint rule).
- [ ] Shared constants are `as const`/frozen; deep copies use structuredClone, not JSON round-trips.
