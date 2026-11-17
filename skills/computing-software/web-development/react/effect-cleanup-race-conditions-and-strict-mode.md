---
id: computing-software.web-development.react.effect-cleanup-race-conditions-and-strict-mode
name: effect-cleanup-race-conditions-and-strict-mode
category: computing-software
field: web-development
product: react
tags: [strict-mode-double-render, effect-race-condition, effect-cleanup, useeffect, abortcontroller, react]
level: practitioner
status: verified
description: "Writing effects that survive StrictMode's double invoke: cleanup for subscriptions and timers, ignoring or aborting stale fetches, and why 'run once' ref hacks are wrong."
sources:
  - https://react.dev/learn/synchronizing-with-effects#how-to-handle-the-effect-firing-twice-in-development
  - https://react.dev/learn/synchronizing-with-effects#fetching-data
  - https://react.dev/reference/react/StrictMode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Effect cleanup, race conditions and StrictMode

## 1. Why effects run twice in development
`<StrictMode>` mounts, unmounts and remounts every component once in dev, running effects -> cleanup -> effects. It simulates a user navigating away and coming back (the React docs' framing) and exposes missing cleanup; it also re-runs ref callbacks once. It also double-calls component bodies, state initialisers and reducers to catch impure code. Production runs once.

## 2. Cleanup for every subscription
```jsx
useEffect(() => {
  const id = setInterval(tick, 1000);
  const onResize = () => setW(innerWidth);
  addEventListener("resize", onResize);
  const conn = createConnection(roomId); conn.connect();
  return () => { clearInterval(id); removeEventListener("resize", onResize); conn.disconnect(); };
}, [roomId]);
```
If the double run causes a visible bug (two connections, duplicate listeners), the cleanup is incomplete.

## 3. Fetch race conditions
Typing quickly changes `query`; responses can arrive out of order and an old one overwrites the new one.
```jsx
useEffect(() => {
  const ctrl = new AbortController();
  fetch(`/api/search?q=${encodeURIComponent(query)}`, { signal: ctrl.signal })
    .then(r => r.json()).then(setResults)
    .catch(e => { if (e.name !== "AbortError") setError(e); });
  return () => ctrl.abort();
}, [query]);
```
Or a boolean `let ignore = false; ... if (!ignore) setResults(d); return () => { ignore = true; }`. Better: TanStack Query/SWR or framework loaders, which handle caching, dedupe and races.

## 4. Anti-patterns
- `const ran = useRef(false); if (ran.current) return; ran.current = true;` to "fix" double runs: hides the bug; breaks with Activity and remounts.
- Side effects that must happen once per user action (POST, analytics on click) belong in event handlers, not effects.
- Non-idempotent effects (incrementing counters on mount) show up as double counts in dev for a reason.

## Verify
- [ ] App behaves identically with StrictMode on; fast typing in search never shows results for an older query.
