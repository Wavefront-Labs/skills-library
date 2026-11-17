---
id: computing-software.web-development.react.hooks-and-state-management
name: hooks-and-state-management
category: computing-software
field: web-development
product: react
tags: [react, hooks, usestate, useeffect, usememo, usecallback, useref, usereducer, usecontext, effect-dependencies, stale-closure, keys, lifting-state, context, zustand, redux, external-store, usesyncexternalstore, tanstack-query, react-query, swr, server-state, strictmode, react-19, actions, use-hook, react-compiler, re-renders, web-development, you-might-not-need-an-effect]
level: practitioner
status: docs-checked
description: "React hooks done right: useState/useEffect/useMemo/useRef, effect dependencies, stale closures, keys, where state should live, TanStack Query, StrictMode, React 19."
sources:
  - https://react.dev/reference/react
  - https://react.dev/learn/you-might-not-need-an-effect
  - https://react.dev/reference/react/useEffectEvent
  - https://react.dev/reference/react/use
  - https://react.dev/blog/2024/12/05/react-19
  - https://react.dev/learn/react-compiler/installation
  - https://tanstack.com/query/latest/docs/framework/react/overview
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# React hooks and state management — the right hook, the right home for state

**Goal:** write components whose state is minimal, lives in the right place, and whose
effects only synchronise with things outside React — no stale values, no render loops.

## 1. Pick the hook by job

| Need | Hook | Note |
|---|---|---|
| Value that changes what renders | `useState` / `useReducer` | Reducer when the next state depends on several fields or actions |
| Mutable value that must NOT re-render (timer id, DOM node, previous value) | `useRef` | Don't read/write `ref.current` during render |
| Expensive derived value | `useMemo` | Only if measured slow (~1 ms+); otherwise compute inline |
| Stable callback for a memoised child or an effect dep | `useCallback` | Pointless unless the consumer is memoised or it's a dependency |
| Sync with an external system (socket, DOM API, subscription) | `useEffect` | Return a cleanup |
| Subscribe to a non-React store | `useSyncExternalStore` | Takes `subscribe`, `getSnapshot` and an optional `getServerSnapshot` for SSR |

## 2. You might not need an effect
Most effects are unnecessary. Replace them:
- **Derived data** → compute during render: `const fullName = first + ' ' + last;` not an effect that sets state.
- **Reacting to a user event** (submit, click) → do it in the event handler, not in an effect watching a flag.
- **Resetting state when a prop changes** → give the component a `key`: `<Profile key={userId} />`.
- **Fetching data** → a server-state library or your framework's loader (see section 5).

## 3. Dependencies and stale closures
Every reactive value used inside an effect/memo/callback goes in the dependency array. Keep
`eslint-plugin-react-hooks` on and never silence `exhaustive-deps` — restructure instead.

```jsx
// Stale: count is captured once, interval always sets 0 + 1
useEffect(() => {
  const id = setInterval(() => setCount(count + 1), 1000);
  return () => clearInterval(id);
}, []);
// Fixed: updater function reads the latest state
useEffect(() => {
  const id = setInterval(() => setCount(c => c + 1), 1000);
  return () => clearInterval(id);
}, []);
```

Objects/functions created during render are new each render, so as deps they re-fire the
effect every time: move them inside the effect or memoise them. For "latest value without
re-subscribing", use `useEffectEvent` (stable since React 19.2): call it only from inside Effects, never
list it in a dependency array, and do not use it just to silence the lint rule.

## 4. Keys
Keys must be stable and unique among siblings: use a database id, never `Math.random()`;
array index only for static lists that never reorder or filter. Wrong keys cause input
values and state to "jump" to the wrong row. Changing a key deliberately remounts a subtree.

## 5. Where state should live
1. **Local** `useState` — default.
2. **Lift** to the nearest common parent when two siblings need it.
3. **Context** for low-frequency, widely read values (theme, locale, current user). Every
   consumer re-renders when the value changes, so split contexts and memoise the value object.
4. **External store** (Zustand, Redux Toolkit, Jotai) for frequently updated, app-wide client
   state where selectors limit re-renders.
5. **Server state is not client state.** Cache it with TanStack Query or SWR: they give
   request deduplication, caching, revalidation on focus and invalidation.

```jsx
const { data, isPending, error } = useQuery({
  queryKey: ['todos', userId],
  queryFn: () => fetch(`/api/todos?user=${userId}`).then(r => r.json()),
  staleTime: 30_000,
});
```

## 6. StrictMode double invocation
In development, `<StrictMode>` renders components twice and runs effect setup → cleanup →
setup once more on mount. If that breaks something (two connections, double analytics
event), your cleanup is missing or incomplete. Production runs once — don't "fix" it by
removing StrictMode or adding a `didRun` ref.

## 7. React 19 notes (verify against your version)
- **Actions:** async functions passed to `<form action={fn}>` or `startTransition`; pending
  state via `useActionState` / `useFormStatus`, optimistic UI via `useOptimistic`.
- **`use(promise)` / `use(context)`:** reads a promise (suspending) or context, and can be
  called conditionally — unlike other hooks. Promises should come from a cache or a server
  component, not be created during render.
- **React Compiler:** auto-memoises, making most manual `useMemo`/`useCallback`
  unnecessary. Stable; install `babel-plugin-react-compiler` (React 19 is the best-supported
  target; 17 and 18 also work with `react-compiler-runtime`). It assumes code follows the Rules of React.

## Verify
- [ ] No effect only derives state from props/state or reacts to a user event.
- [ ] `exhaustive-deps` lint passes with no disables.
- [ ] Every effect that subscribes, connects or sets a timer returns a cleanup; StrictMode dev shows no duplicates.
- [ ] List keys are stable ids; reordering a list keeps input values with the right rows.
- [ ] Server data is fetched through a cache layer, not ad-hoc `useEffect` + `useState`.
- [ ] React DevTools Profiler shows no component re-rendering on unrelated context changes.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the React 19 and 19.2 posts, the React Compiler install guide, and the TanStack Query, SWR and Zustand docs. Confirmed: `useMemo` guidance to measure first (about 1 ms or more); StrictMode setup, cleanup, setup cycle; `use` can be called conditionally and needs a cached Promise; `useActionState`, `useFormStatus` and `useOptimistic` in React 19; `useEffectEvent` shipped in 19.2 and is not listed as a dependency; the React Compiler is stable and installs as `babel-plugin-react-compiler`; context re-renders every consumer when the value changes; TanStack Query covers caching and request deduplication and SWR revalidates on focus; TanStack Query v5 `isPending`/`staleTime`. Removed the unconfirmed "tear-free" wording, the retries claim and the compiler version guess.

Method: documentation only; no commands were run.
