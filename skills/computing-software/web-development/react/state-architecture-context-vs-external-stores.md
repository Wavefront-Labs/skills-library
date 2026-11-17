---
id: computing-software.web-development.react.state-architecture-context-vs-external-stores
name: state-architecture-context-vs-external-stores
category: computing-software
field: web-development
product: react
tags: [react, state-management, context, redux, zustand, jotai, prop-drilling, stale-closure, usesyncexternalstore, web-development, architecture, context-performance]
level: advanced
status: docs-checked
description: "Choosing context vs. an external store (Zustand/Redux/Jotai) for React state, and avoiding context re-render storms and stale-closure bugs."
sources:
  - https://react.dev/learn/scaling-up-with-reducer-and-context
  - https://react.dev/reference/react/useContext
  - https://react.dev/reference/react/useSyncExternalStore
  - https://github.com/pmndrs/zustand
  - https://redux-toolkit.js.org/api/createSlice
  - https://redux-toolkit.js.org/api/getDefaultMiddleware
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# React state architecture — where state should live

**Goal:** put each piece of state at the right altitude so components stay simple,
re-renders stay cheap, and nothing goes stale.

## 1. The decision, in order
1. **Local `useState`** if only one component (and maybe its direct children via
   props) needs it. Default here; resist lifting state "just in case."
2. **Lift to nearest common ancestor** if two siblings need to share it. Prop
   drilling 1-2 levels is fine and more debuggable than an abstraction.
3. **Context** when drilling would pass through many levels or many unrelated branches need
   the same value (theme, locale, auth user) — and the value changes rarely.
4. **External store** (Zustand, Jotai, Redux Toolkit) when state is read/written
   from many unrelated parts of the tree *and* changes frequently, or must survive
   outside React (persisted, read from non-React code, time-travel debugging).
Context is not a performance tool and is not a replacement for a store — it's
dependency injection for a value, nothing more.

## 2. Why context re-renders more than people expect
Every consumer of `useContext(Ctx)` re-renders whenever the provider's `value`
changes, full stop — there's no selector built in. A provider that recreates its
value object every render (`<Ctx value={{ user, setUser }}>` without memoizing)
re-renders every consumer on every parent render, context value change or not.
Fix: memoize the value with `useMemo`, and split one big context into several
narrow ones (`UserContext`, `ThemeContext`) so a theme toggle doesn't re-render
every component reading the user.

## 3. External stores give you selectors — that's the real win
Zustand and React Redux subscribe components to a *slice* of state via a selector
function, so a component reading `cart.total` doesn't re-render when `cart.items`
changes elsewhere. This is the mechanism context lacks. Zustand and React Redux are built on
`useSyncExternalStore`, the React primitive for subscribing React to
state that lives outside React's render cycle — write your own tiny stores with it
directly if you don't want a dependency.

## 4. Stale closures — the bug that looks like a React bug but isn't
```js
useEffect(() => {
  const id = setInterval(() => console.log(count), 1000); // closes over count at mount time
  return () => clearInterval(id);
}, []); // count is stale forever
```
Any callback captured once (effect with `[]` deps, event listener added once, a
`setTimeout`) closes over the values from that render. Fix by either adding the
real dependency, using a ref to hold the latest value (`useRef` + assign in an
effect that runs every render), or using the store's `getState()` to read fresh
values outside the render cycle (Zustand/Redux actions do this correctly already).

## 5. Derived state is not state
Don't `useState` + `useEffect` to mirror a value computed from props/other state —
compute it inline during render, or `useMemo` if expensive. Syncing state via effect
is the single most common source of extra renders, race conditions, and "why is this
one render behind" bugs in React codebases.

## 6. Redux Toolkit specifics worth knowing
- `createSlice` + Immer means you can "mutate" draft state in reducers; outside a
  reducer, mutating state is still a bug, and the development-only immutability check middleware flags it.
- `createEntityAdapter` for normalized collections instead of hand-rolled nested objects.
- RTK Query replaces most hand-written data-fetching + caching code and integrates
  with the same store.

## Verify
- [ ] No context provider passes an unmemoized object/array literal as `value`.
- [ ] Frequently-changing, widely-read state uses a store with selectors, not context.
- [ ] No `useEffect` exists solely to copy a prop or another state value into local state.
- [ ] Callbacks that must see fresh state after a delay use a ref or store `getState()`, not a stale closure.
- [ ] Each context is scoped to one concern (auth, theme, locale) — not one god-context.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the Zustand and React Redux sources and the Redux Toolkit docs (2.13.0). Confirmed: `useContext` re-renders every consuming component when the provided value changes (React 19 renders `<Context value>` as the provider); Zustand and React Redux call `useSyncExternalStore`; Zustand components re-render only for the state they select; `createSlice` lets reducers "mutate" via Immer; `getDefaultMiddleware` adds immutability and serializability checks in development builds only; `createEntityAdapter` exists. Removed the "4+ levels" threshold, the claim that state is frozen in dev, and Jotai from the selector and `useSyncExternalStore` sentences (not checked).

Method: documentation only; no commands were run.
