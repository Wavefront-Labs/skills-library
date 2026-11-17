---
id: computing-software.web-development.react.useeffectevent-separating-events-from-effects
name: useeffectevent-separating-events-from-effects
category: computing-software
field: web-development
product: react
tags: [useeffectevent, effect-events, useeffect, stale-closures, react]
level: advanced
status: verified
description: "Using useEffectEvent to read the latest props and state inside effects without re-running them: when values are reactive vs non-reactive, rules for effect events and alternatives."
sources:
  - https://react.dev/reference/react/useEffectEvent
  - https://react.dev/learn/separating-events-from-effects
  - https://react.dev/blog/2025/10/01/react-19-2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useEffectEvent: separating events from effects

Stable in React 19.2. Solves "my effect needs the latest value of X, but X changing shouldn't re-run the effect".

## 1. The problem
```jsx
useEffect(() => {
  const conn = connect(roomId);
  conn.on("connected", () => showToast("Connected", theme));   // theme is needed...
  return () => conn.disconnect();
}, [roomId, theme]);   // ...so changing theme reconnects the chat. Bad.
```

## 2. The fix
```jsx
import { useEffect, useEffectEvent } from "react";
const onConnected = useEffectEvent(() => showToast("Connected", theme));   // always sees latest theme
useEffect(() => {
  const conn = connect(roomId);
  conn.on("connected", () => onConnected());
  return () => conn.disconnect();
}, [roomId]);          // only reactive value; effect events are not dependencies
```
- **Reactive** values (the effect should resync when they change): `roomId`.
- **Non-reactive** logic (read latest, don't resync): logging, analytics with current user, notifications using current settings.

## 3. Rules
- Call effect events only from inside effects, `useLayoutEffect`, `useInsertionEffect` or other effect events, never during render (React throws "can't be called during rendering"; checked). Calling one from an event handler happened to run in tests but is outside the documented contract.
- Don't pass them to other components or hooks.
- Don't list them in dependency arrays or pass them around as callbacks: wrap them as `() => onTick()` like the react.dev timer example (eslint-plugin-react-hooks 6.1.0 added "disallow calling `useEffectEvent` functions in arbitrary closures").
- Don't use it to silence the linter for values that *should* be reactive - that hides real bugs.

## 4. Typical uses
```jsx
const onVisit = useEffectEvent((url) => analytics.page(url, { cartCount }));
useEffect(() => { onVisit(url); }, [url]);           // logs once per URL with latest cartCount

const onTick = useEffectEvent(() => setCount(c => c + step));
useEffect(() => { const id = setInterval(() => onTick(), 1000); return () => clearInterval(id); }, []);  // step changes don't reset interval
```

## 5. Before 19.2
The "latest ref" pattern: `const ref = useRef(fn); useLayoutEffect(() => { ref.current = fn; });` then call `ref.current()` in the effect. Equivalent semantics, more boilerplate.

## Verify
- [ ] Changing non-reactive values no longer re-runs subscriptions (check network/websocket reconnects); linter passes without disabling exhaustive-deps.
