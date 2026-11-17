---
id: computing-software.web-development.react.synchronising-with-effects-and-cleanup
name: synchronising-with-effects-and-cleanup
category: computing-software
field: web-development
product: react
tags: [react, effect-cleanup, useeffect, synchronisation, strict-mode, abortcontroller, race-conditions, web-development]
level: practitioner
status: docs-checked
description: "Using useEffect to synchronise with external systems: setup/cleanup symmetry, StrictMode double run, fetch race conditions, subscriptions and timers."
sources:
  - https://react.dev/learn/synchronizing-with-effects
  - https://react.dev/learn/lifecycle-of-reactive-effects
  - https://react.dev/reference/react/useEffect
  - https://react.dev/reference/react/StrictMode
  - https://react.dev/reference/react/useInsertionEffect
  - https://developer.mozilla.org/en-US/docs/Web/API/AbortController
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Synchronising with effects and cleanup

**Goal:** effects that connect to something outside React and disconnect cleanly, so StrictMode, fast navigation and prop changes never leak or race.

## 1. Think start/stop, not lifecycle
An effect says "while this component shows with these values, stay synchronised with X". React may run setup -> cleanup -> setup at any time (prop change, StrictMode, Fast Refresh).
```jsx
useEffect(() => {
  const conn = createConnection(serverUrl, roomId);
  conn.connect();
  return () => conn.disconnect();
}, [serverUrl, roomId]);
```

## 2. StrictMode double run is a test
In development React mounts, unmounts, and remounts every component once. If that breaks something, your cleanup is missing or incomplete. Don't "fix" it with a `didRun` ref.

## 3. Common cleanups
| Setup | Cleanup |
|---|---|
| `addEventListener` | `removeEventListener` (same function reference) |
| `setInterval/setTimeout` | `clearInterval/clearTimeout` |
| `subscribe()` | returned unsubscribe |
| animation | reset to initial value |
| `dialog.showModal()` | `dialog.close()` |
| fetch | abort or ignore result |

## 4. Fetch race conditions
```jsx
useEffect(() => {
  const ctrl = new AbortController();
  fetch(`/api/users/${id}`, { signal: ctrl.signal })
    .then(r => r.json()).then(setUser)
    .catch(e => { if (e.name !== "AbortError") setError(e); });
  return () => ctrl.abort();
}, [id]);
```
Without it a slow response for an old `id` can overwrite the new one. In real apps prefer a data library or framework loader (caching, dedupe, no waterfalls).

## 5. Don't use effects for
Derived data, responding to user events, resetting state on prop change (use `key`), or one-time app init (run at module level or guard with a module variable).

## 6. Timing variants
`useEffect` runs after paint; `useLayoutEffect` before paint (measuring); `useInsertionEffect` for CSS-in-JS libraries only.

## 7. Subscribing to external stores
Prefer `useSyncExternalStore(subscribe, getSnapshot)` over effect + setState for browser APIs and stores - it's tearing-safe in concurrent rendering.

## Verify
- [ ] Dev StrictMode logs show connect/disconnect/connect, and only one live connection remains.
- [ ] Rapidly switching ids never shows data for the wrong id (throttle network in DevTools).
- [ ] Unmounting a page leaves no running intervals/listeners (Performance > Memory or a log in cleanup).

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20). Confirmed: in development Strict Mode runs one extra setup, cleanup, setup cycle and the fix is a proper cleanup rather than a `didRun` ref; cleanup examples (connect and disconnect, subscribe and unsubscribe, animations reset to initial values, `showModal` and `close`); fetch cleanup by aborting or ignoring the result; one-time app initialisation guarded by a module variable; `useLayoutEffect` blocks painting; `useInsertionEffect` is for CSS-in-JS library authors. Replaced the unsourced `new Map(el)` row with the documented `showModal` example.

Method: documentation only; no commands were run.
