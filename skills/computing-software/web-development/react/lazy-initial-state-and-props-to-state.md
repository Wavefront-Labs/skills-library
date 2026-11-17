---
id: computing-software.web-development.react.lazy-initial-state-and-props-to-state
name: lazy-initial-state-and-props-to-state
category: computing-software
field: web-development
product: react
tags: [lazy-initial-state, usestate, derived-state, props-to-state, react]
level: practitioner
status: verified
description: "Initialising React state correctly: lazy initialisers for expensive defaults, why copying props into state goes stale, deriving values instead, and resetting state with keys."
sources:
  - https://react.dev/reference/react/useState#avoiding-recreating-the-initial-state
  - https://react.dev/learn/choosing-the-state-structure#don-t-mirror-props-in-state
  - https://react.dev/learn/you-might-not-need-an-effect
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lazy initial state and initialising from props

## 1. Lazy initialiser
```jsx
const [todos, setTodos] = useState(createInitialTodos());   // runs every render, result ignored after first
const [todos, setTodos] = useState(createInitialTodos);     // function: runs once
const [draft, setDraft] = useState(() => JSON.parse(localStorage.getItem("draft") ?? "{}"));
```
Use the function form when the initial value is expensive (parsing storage, building large structures). Same for `useReducer(reducer, arg, init)`. In StrictMode dev the initialiser runs twice - keep it pure. (Checked: `useState(fn)` and the `init` argument of `useReducer` each ran once in a normal render.)

SSR caveat: reading `localStorage`/`window` in the initialiser breaks on the server and causes hydration mismatches. Initialise to a default, then sync in an effect, or use `useSyncExternalStore` with a `getServerSnapshot`.

## 2. Props into state: usually a bug
```jsx
function Price({ amount }) {
  const [value, setValue] = useState(amount);   // only reads amount on first mount; later changes ignored
```
Options:
- **Derive** during render: `const formatted = format(amount);` - no state at all.
- **Expensive derivation**: `useMemo(() => compute(amount), [amount])` (or let React Compiler memoise).
- **Intentionally seeded** editable copies: name it `initialAmount`/`defaultValue` so callers know later changes are ignored.
- **Reset when an identity changes**: give the component a key: `<EditForm key={user.id} user={user} />` - React remounts and re-runs initialisers.

## 3. Adjusting state when a prop changes (rare)
```jsx
const [prevItems, setPrevItems] = useState(items);
const [selection, setSelection] = useState(null);
if (items !== prevItems) { setPrevItems(items); setSelection(null); }   // during render, not in an effect
```
Prefer keys or derivation; avoid `useEffect(() => setX(prop), [prop])`, which renders once with stale state and then again.

## Verify
- [ ] No expensive initialisers called on every render (profile); no state copied from props without a reset strategy; components reset correctly when switching entities.
