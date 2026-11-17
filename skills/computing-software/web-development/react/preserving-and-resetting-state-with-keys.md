---
id: computing-software.web-development.react.preserving-and-resetting-state-with-keys
name: preserving-and-resetting-state-with-keys
category: computing-software
field: web-development
product: react
tags: [react, reset-state-with-key, state-preservation, component-identity, keys, reconciliation, web-development]
level: practitioner
status: verified
description: "Controlling when React keeps or discards component state: position in the tree, same type at same position, and resetting with a key."
sources:
  - https://react.dev/learn/preserving-and-resetting-state
  - https://react.dev/learn/you-might-not-need-an-effect#resetting-all-state-when-a-prop-changes
  - https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preserving and resetting state with keys and position

**Goal:** state resets exactly when the user expects it to, never by accident.

## 1. The rule
State is tied to a **position in the render tree**, not to the JSX variable. Same component type at the same position = state preserved. Different type or different position = state destroyed (including all children).

```jsx
{isPlayerA ? <Counter person="A" /> : <Counter person="B" />}   // same position, same type: count carries over
```

## 2. Reset with key
```jsx
<Chat key={contactId} contact={contact} />
```
Changing `key` unmounts and remounts: fresh state, effects re-run. This replaces effects like `useEffect(() => setDraft(""), [contactId])`, which render stale data first.

Two ways to force separate state for the two-player example:
```jsx
{isPlayerA ? <Counter key="A" /> : <Counter key="B" />}
{isPlayerA && <Counter />}{!isPlayerA && <Counter />}   // different positions
```

## 3. Accidental resets
- **Nested component definitions**: declaring `function Input() {}` inside another component creates a new type every render - the input loses focus and state each keystroke. Define components at module top level.
- Wrapping in a different element conditionally (`<div>` vs `<section>`) changes the tree and resets children (checked: a counter went from 1 to 0).
- Unstable list keys (`Math.random()`, index on a reorderable list) reset item state.

## 4. Preserving state for removed components
Need hidden tabs to keep state? Options: render all and hide with CSS (`hidden` attribute), lift state up, or persist to storage. React 19.2's `<Activity mode="hidden">` keeps state while hidden (checked: a counter kept its value across hide and show) and destroys the children's Effects while hidden.

## 5. Partial reset
Remounting resets everything. To reset only some fields when a prop changes, store the previous prop and adjust during render:
```jsx
const [prevId, setPrevId] = useState(id);
if (id !== prevId) { setPrevId(id); setSelection(null); }
```
Use sparingly; `key` is clearer.

## Verify
- [ ] Switching between records shows no stale input from the previous record.
- [ ] Typing in an input never loses focus mid-word (no nested component definitions).
- [ ] React DevTools "Highlight updates" / component tree shows expected remounts.
