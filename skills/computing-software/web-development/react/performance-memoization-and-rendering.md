---
id: computing-software.web-development.react.performance-memoization-and-rendering
name: performance-memoization-and-rendering
category: computing-software
field: web-development
product: react
tags: [react, performance, rendering, usememo, usecallback, react.memo, profiler, reconciliation, re-render, virtual-dom, context, useeffect, web-development]
level: advanced
status: docs-checked
description: "Diagnosing why React re-renders and fixing it with memo/useMemo/useCallback, keys, and the Profiler — not reaching for memoization first."
sources:
  - https://react.dev/reference/react/memo
  - https://react.dev/reference/react/useMemo
  - https://react.dev/reference/react/useCallback
  - https://react.dev/reference/react/useContext
  - https://react.dev/reference/react/Profiler
  - https://react.dev/learn/render-and-commit
  - https://react.dev/learn/rendering-lists
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# React render performance — profile before you memoize

**Goal:** know why a component re-rendered, and fix the cheapest real cause before
reaching for `memo`/`useMemo`/`useCallback`, which have their own cost and can make
things worse if misapplied.

## 1. Why components re-render
A component re-renders when: its state changes, its parent re-renders (propagates
down regardless of whether props changed), its context value changes, or a hook it
calls (`useState`, `useReducer`, `useSyncExternalStore`) signals an update. Re-render
is not the same as DOM mutation — React still diffs the virtual tree and bails out of
DOM writes for unchanged nodes, so a cheap re-render that touches no DOM is often not
a real problem. Profile before assuming re-renders are the bottleneck.

## 2. React DevTools Profiler, not guesswork
Record a profiling session, perform the slow interaction, and read the flamegraph
for which components rendered and how long they took. Enable "Highlight updates when
components render" (General settings) to see renders happen live, and "Record why each
component rendered while profiling" (Profiler settings) to see the cause before touching
code — chasing re-renders that don't show up in the profile wastes time and adds
complexity for nothing.

## 3. The three tools, and when each is wrong
- **`React.memo(Component)`** — skips re-render if props are shallow-equal. Useless
  if you pass a new object/array/function literal as a prop every render (shallow
  equal will always fail) — you must stabilize those first.
- **`useMemo(fn, deps)`** — caches an expensive computed value. Wrong for cheap
  computations: the memoization bookkeeping can cost more than recomputing a simple
  sum or string concat.
- **`useCallback(fn, deps)`** — caches a function identity, useful only when that
  identity feeds a `memo`-wrapped child or a `useEffect` dependency array. Useless on
  its own; it exists to make the *other* two work.
- Gotcha: an inline object/array dependency (`{ id }`) in a `deps` array breaks memoization
  every render because it's a new reference — memoize or primitive-ize the dependency itself.

## 4. Cheaper fixes than memoization
- **Move state down**: if only a leaf needs the fast-changing state, lift it out of
  the parent so siblings don't re-render with it.
- **Lift content up / children as props**: pass JSX as `children` instead of letting
  a parent component construct it, so the parent's re-render doesn't force the
  child's subtree to re-evaluate.
- **Split contexts**: one `AppContext` with `{ user, theme, cart }` re-renders every
  consumer on any change. Split into `UserContext`, `ThemeContext`, `CartContext`.
- **Derive instead of sync**: a `useEffect` that calls `setState` from a prop is
  almost always better written as a plain derived value computed during render.

## 5. Keys and list identity
Using array index as `key` on a reorderable/filterable list causes React to reuse
the wrong DOM node and its internal state (inputs keep stale values, animations
glitch). Use a stable id from the data. Changing a `key` intentionally is a trick to
force full remount (e.g. reset a form by keying it on `recordId`).

## 6. Expensive children and `startTransition`
For renders that are correctly expensive (large lists, heavy charts) rather than
accidentally re-rendering: `useDeferredValue` or `startTransition` (React 18+) lets
React interrupt the expensive render to keep input responsive, instead of forcing
you to memoize everything. Virtualize long lists (`react-window`/`@tanstack/react-virtual`)
rather than trying to make a very large render fast by other means.

## Verify
- [ ] Profiler flamegraph identifies the actual slow commit before any memo is added.
- [ ] Every `memo`'d component receives stable props (no inline object/array/fn literals from the parent).
- [ ] List `key`s are stable domain ids, never array index, on any reorderable/filterable list.
- [ ] No `useEffect` is syncing a value that could be a derived variable computed in render.
- [ ] Context providers are split so an unrelated value change doesn't re-render unrelated consumers.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20) and the React DevTools source (facebook/react, packages/react-devtools-shared). Confirmed: React re-renders children when the parent re-renders and `memo` compares each prop with `Object.is` (shallow equality), so fresh object, array or function props defeat it; a memoised component still re-renders on its own state or context change; the docs recommend letting wrapper components accept JSX as `children`; `useMemo` is worth it only when measured work is significant (about 1 ms or more); a context change re-renders every consumer; unstable list keys (index, `Math.random()`) cause recreated or mismatched DOM; the DevTools settings "Highlight updates when components render" and "Record why each component rendered while profiling". Removed the flamegraph width/colour description and the 5,000-row figure, which no doc covers.

Method: documentation only; no commands were run.
