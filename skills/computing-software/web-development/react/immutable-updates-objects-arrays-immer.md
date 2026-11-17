---
id: computing-software.web-development.react.immutable-updates-objects-arrays-immer
name: immutable-updates-objects-arrays-immer
category: computing-software
field: web-development
product: react
tags: [react, immutable-updates, immer, use-immer, spread-syntax, structuredclone, state-updates, web-development]
level: practitioner
status: verified
description: "Updating objects and arrays in React state immutably: spread patterns for nested data, non-mutating array methods, and when to use Immer."
sources:
  - https://react.dev/learn/updating-objects-in-state
  - https://react.dev/learn/updating-arrays-in-state
  - https://immerjs.github.io/immer/
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/toSorted
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Immutable updates for objects and arrays

**Goal:** every state change produces a new reference so React (and memoised children) see it.

## 1. Objects
```jsx
setUser({ ...user, name });                                    // shallow
setUser(u => ({ ...u, address: { ...u.address, city } }));    // nested: copy each level you change
```
Mutating `user.name = x; setUser(user)` does not re-render (same reference) and corrupts earlier snapshots.

## 2. Arrays: use non-mutating operations
| Goal | Avoid (mutates) | Use |
|---|---|---|
| add | `push`, `unshift` | `[...a, x]`, `[x, ...a]` |
| remove | `splice` | `a.filter(i => i.id !== id)` |
| replace | `a[i] = x` | `a.map(i => i.id === id ? {...i, done: true} : i)` |
| insert at | `splice` | `[...a.slice(0, n), x, ...a.slice(n)]` or `a.toSpliced(n, 0, x)` (ES2023; run on Node 20) |
| sort/reverse | `sort`, `reverse` | `a.toSorted(cmp)`, `a.toReversed()` (ES2023), or `[...a].sort()` |

`[...a]` is shallow: `copy[0].done = true` still mutates the shared object - map to a new object instead.

## 3. Immer for deep structures
```jsx
import { useImmer } from "use-immer";
const [doc, updateDoc] = useImmer(initial);
updateDoc(d => { d.sections[2].items.push(item); });
```
Or with plain `useState`: `setDoc(produce(draft => { ... }))`. Immer records mutations on a draft proxy and produces structurally shared copies. Don't both mutate the draft and return a new value (Immer throws "returned a new value *and* modified its draft"; checked on immer 11.1.21). Redux Toolkit's `createSlice` uses Immer internally.

## 4. Normalise instead of deep nesting
If updates repeatedly dig 4 levels deep, store entities by id (`{ byId: {}, allIds: [] }`) - updates become one-level spreads.

## 5. Catching mutation
- StrictMode double-renders expose some impurity.
- `Object.freeze` state in development, or Immer's auto-freeze (on by default; `produce` output is frozen), to make mutations throw. Frozen objects only throw in strict mode code, such as ES modules (checked: `TypeError`); sloppy scripts fail silently.
- ESLint `react-compiler` / `eslint-plugin-react-hooks` flags mutation of props/state in newer versions.

## Verify
- [ ] `grep -rnE "\.(push|splice|sort|reverse)\(" src` - every hit is on a local copy, not state.
- [ ] Memoised children re-render after updates (no stale UI).
- [ ] Undo/history features show prior states unchanged.
