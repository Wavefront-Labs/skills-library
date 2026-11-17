---
id: computing-software.web-development.react.state-as-snapshot-and-batching
name: state-as-snapshot-and-batching
category: computing-software
field: web-development
product: react
tags: [react, state-snapshot, state-batching, updater-function, usestate, automatic-batching, flushsync, web-development]
level: practitioner
status: verified
description: "Reasoning about React state as a per-render snapshot: why setState doesn't change the variable, batching, updater functions and flushSync."
sources:
  - https://react.dev/learn/state-as-a-snapshot
  - https://react.dev/learn/queueing-a-series-of-state-updates
  - https://react.dev/reference/react-dom/flushSync
  - https://github.com/reactwg/react-18/discussions/21
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State as a snapshot and batching

**Goal:** predict exactly what value a state variable has when code runs.

## 1. Each render has fixed state
```jsx
const [count, setCount] = useState(0);
function handleClick() {
  setCount(count + 1);
  setCount(count + 1);
  console.log(count);           // still 0 - this render's snapshot
}
// result: 1, not 2 (run on React 19.3.1)
```
`setCount` requests a re-render with a new value; it never mutates `count` in the current closure. Timeouts and async callbacks also see the snapshot from the render that created them.

## 2. Updater functions for chained updates
```jsx
setCount(c => c + 1);
setCount(c => c + 1);           // result: 2
```
Use the updater when the next state depends on the previous one, especially in async code, intervals and multiple updates per event. Updaters must be pure (StrictMode calls them twice in dev).

## 3. Batching
React 18+ batches all updates in the same tick - event handlers, promises, timeouts, native listeners - into one re-render (automatic batching with `createRoot`). Legacy `ReactDOM.render` only batched inside React events.
```jsx
fetch(url).then(() => { setLoading(false); setData(d); });   // one render in 18+ (checked with setTimeout: 1 render for 2 setStates)
```

## 4. Need the DOM updated now: flushSync
```jsx
import { flushSync } from "react-dom";
flushSync(() => setItems([...items, newItem]));
listRef.current.lastChild.scrollIntoView();
```
Rare and expensive; use for scroll/focus that must follow a state change synchronously.

## 5. Reading the "latest" value
Need the current value inside a long-lived callback? Use the updater form, or keep it in a ref (`latest.current = value` in an effect) - or `useEffectEvent` in React 19.2+ for effect-triggered logic.

## 6. Objects in state
Snapshot also applies to objects: mutate and set the same reference and React bails out (`Object.is` equal), so nothing re-renders. Always create a new object.

## Verify
- [ ] Multiple increments in one handler use the updater form.
- [ ] Intervals use `setX(x => ...)` and don't list `x` as an effect dependency.
- [ ] React DevTools Profiler shows one commit for multi-setState handlers.
