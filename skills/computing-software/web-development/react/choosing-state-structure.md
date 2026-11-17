---
id: computing-software.web-development.react.choosing-state-structure
name: choosing-state-structure
category: computing-software
field: web-development
product: react
tags: [react, state-structure, derived-state, normalised-state, redundant-state, single-source-of-truth, web-development]
level: practitioner
status: verified
description: "Structuring React state: group related values, avoid contradictions, redundancy and duplication, store ids not copies, derive values during render."
sources:
  - https://react.dev/learn/choosing-the-state-structure
  - https://react.dev/learn/you-might-not-need-an-effect#updating-state-based-on-props-or-state
  - https://redux.js.org/usage/structuring-reducers/normalizing-state-shape
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing state structure

**Goal:** the smallest state that can't contradict itself; everything else is computed.

## 1. Five rules from the React docs
1. **Group related state** that always changes together: `{x, y}` not two `useState`s.
2. **Avoid contradictions**: `isSending` + `isSent` can both be true; use one `status: 'typing' | 'sending' | 'sent'`.
3. **Avoid redundant state**: `fullName` from `first` + `last` is computed in render.
4. **Avoid duplication**: store `selectedId`, not a copy of the selected item (the copy goes stale when the list is edited).
5. **Avoid deep nesting**: flatten to `{ byId, childIds }` for trees.

## 2. Derive, don't sync
```jsx
const [items, setItems] = useState([]);
const [query, setQuery] = useState("");
const visible = useMemo(() => items.filter(i => i.name.includes(query)), [items, query]);
```
An effect that copies props/state into other state (`useEffect(() => setVisible(...))`) renders twice and can go stale. Compute; memoise only if measurably slow.

## 3. Don't mirror props
```jsx
function Message({ color }) { const [c] = useState(color); }   // ignores later prop changes
```
Use the prop directly. If you need an initial value only, name it `initialColor`. To reset when an id changes, use `key`.

## 4. Selected item pattern
```jsx
const [selectedId, setSelectedId] = useState(null);
const selected = items.find(i => i.id === selectedId);
```

## 5. Enumerated status beats booleans
```ts
type State =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "error"; error: string }
  | { status: "success"; data: Item[] };
```
TypeScript discriminated unions make impossible states unrepresentable.

## 6. Where it lives
Closest common parent of the components that need it; lift up when two siblings need it; server data belongs in a server-state cache (TanStack Query / framework loader), not `useState`.

## Verify
- [ ] No `useEffect` whose only job is `setState(derivedFrom(otherState))`.
- [ ] No boolean pairs that could both be true.
- [ ] Editing an item updates the selected detail view (no stale copy).
