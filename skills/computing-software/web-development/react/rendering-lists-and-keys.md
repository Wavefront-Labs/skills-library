---
id: computing-software.web-development.react.rendering-lists-and-keys
name: rendering-lists-and-keys
category: computing-software
field: web-development
product: react
tags: [jsx, react-components, list-keys, react-keys, rendering-lists, key-prop, index-as-key, virtualized-lists]
level: practitioner
status: verified
description: "Rendering lists in React with stable keys: why index keys break reordering and inputs, generating ids, fragments with keys, and virtualising long lists."
sources:
  - https://react.dev/learn/rendering-lists
  - https://react.dev/learn/preserving-and-resetting-state#option-2-resetting-state-with-a-key
  - https://tanstack.com/virtual/latest
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rendering lists and keys

**Goal:** list items keep the right state and DOM as the list changes, and long lists stay fast.

## 1. Keys identify items among siblings
```jsx
<ul>{todos.map(t => <TodoItem key={t.id} todo={t} />)}</ul>
```
- Stable, unique among siblings, derived from the data (database id, slug).
- Not `Math.random()`/`crypto.randomUUID()` in render (new key each render -> remount every time, lost focus/state, slow).
- Not array index when items can be inserted, removed, reordered or filtered: state (input text, checkbox, expanded) sticks to the **position**, so it jumps to the wrong item.
- Index is fine for static lists that never change order.

## 2. No id in the data?
Assign ids when data enters the app (on creation/fetch: `{ ...item, id: crypto.randomUUID() }`), not during render. For server data, use the natural key or a composite (`${row.date}-${row.sku}`) that is unique.

## 3. Keys on the right element
The key goes on the outermost element returned by `map` - the component, not an element inside it. For multiple elements per item use a keyed Fragment:
```jsx
{terms.map(t => <Fragment key={t.id}><dt>{t.term}</dt><dd>{t.def}</dd></Fragment>)}
```
`key` isn't passed as a prop (reading `props.key` logs "`key` is not a prop" and gives `undefined`; checked) - pass `id` separately if the child needs it.

## 4. Duplicate key warning
"Encountered two children with the same key" (checked, exact start of the React 19.3.1 warning) means items collide (dupes in data, or non-unique composite). Fix the data or key - React warns that non-unique keys "may cause children to be duplicated and/or omitted".

## 5. Long lists
Rendering thousands of rows costs render time and DOM size (INP). Virtualise with TanStack Virtual / react-window (only visible rows in the DOM), or paginate. CSS `content-visibility: auto` on rows is a cheap middle ground for static content.

## Verify
- [ ] Typing in a row input then deleting a row above keeps the text with the correct row.
- [ ] No key warnings in the console.
- [ ] Profiler: reordering a list moves DOM nodes rather than remounting all items.
