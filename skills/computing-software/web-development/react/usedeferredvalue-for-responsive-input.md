---
id: computing-software.web-development.react.usedeferredvalue-for-responsive-input
name: usedeferredvalue-for-responsive-input
category: computing-software
field: web-development
product: react
tags: [react, usedeferredvalue, concurrent-rendering, search-as-you-type, stale-content, memo, web-development]
level: practitioner
status: verified
description: "Using useDeferredValue to keep inputs responsive while expensive children render, showing stale results, initialValue, and pairing it with memo."
sources:
  - https://react.dev/reference/react/useDeferredValue
  - https://react.dev/reference/react/memo
  - https://react.dev/blog/2024/12/05/react-19#usedeferredvalue-initial-value
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useDeferredValue

**Goal:** typing stays instant while a slow list/chart re-renders with a lagging value.

## 1. Pattern
```jsx
function Search() {
  const [query, setQuery] = useState("");
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  return (
    <>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <div style={{ opacity: isStale ? 0.5 : 1 }}>
        <SlowResults query={deferredQuery} />
      </div>
    </>
  );
}
const SlowResults = memo(function SlowResults({ query }) { /* heavy */ });
```
React first re-renders with the old deferred value (cheap, because `SlowResults` is memoised and its prop didn't change), then renders the new value in the background, abandoning it if the user types again.

## 2. memo is required
Without `memo` (or React Compiler auto-memoisation), the child re-renders on the urgent pass anyway and nothing is gained.

## 3. With Suspense
If `SlowResults` suspends on fetch, the deferred value keeps showing old results instead of the fallback while new data loads.

## 4. initialValue (React 19)
`useDeferredValue(value, "")` renders the initial value first on mount, then the real one in the background (checked: renders `init` then `final`) - useful for a fast first paint.

## 5. vs debouncing/throttling
Debounce waits a fixed delay even on fast machines; deferring adapts to device speed and is interruptible. Debounce is still right for **network** requests (fewer calls); deferral is for **rendering** cost. Combine them when both apply.

## 6. vs useTransition
`useTransition` wraps the setter you own; `useDeferredValue` wraps a value you receive (e.g. a prop) or when you can't touch the setter.

## Verify
- [ ] With CPU throttled, typing in the input has no dropped characters.
- [ ] Results visibly dim while stale.
- [ ] The heavy child is memoised (React DevTools shows it skipped on urgent renders).
