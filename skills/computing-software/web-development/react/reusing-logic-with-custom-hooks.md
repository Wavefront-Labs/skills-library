---
id: computing-software.web-development.react.reusing-logic-with-custom-hooks
name: reusing-logic-with-custom-hooks
category: computing-software
field: web-development
product: react
tags: [react, custom-hooks, hooks, rules-of-hooks, usesyncexternalstore, composition, web-development]
level: practitioner
status: docs-checked
description: "Extracting React logic into custom hooks: naming and rules of hooks, sharing logic not state, passing reactive values and event handlers, and when not to."
sources:
  - https://react.dev/learn/reusing-logic-with-custom-hooks
  - https://react.dev/reference/rules/rules-of-hooks
  - https://react.dev/reference/react/useSyncExternalStore
  - https://react.dev/reference/react/useEffectEvent
  - https://testing-library.com/docs/react-testing-library/api#renderhook
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reusing logic with custom hooks

**Goal:** hooks that name a concrete purpose, compose cleanly and don't hide bugs.

## 1. Rules
- Name starts with `use` + capital letter, and it must call at least one hook (otherwise make it a normal function).
- Call hooks only at the top level of components/hooks: no conditions, loops, or after early returns.
- Enforce with `eslint-plugin-react-hooks` (`rules-of-hooks`, `exhaustive-deps`).

## 2. Hooks share logic, not state
Two components calling `useOnlineStatus()` each get their own state. To share state, lift it or use context/external store.

## 3. A good hook
```jsx
function subscribe(cb) {
  window.addEventListener("online", cb); window.addEventListener("offline", cb);
  return () => { window.removeEventListener("online", cb); window.removeEventListener("offline", cb); };
}
export function useOnlineStatus() {
  return useSyncExternalStore(subscribe, () => navigator.onLine, () => true);
}
```
Concrete, single purpose, server snapshot provided for SSR.

## 4. Passing reactive values
```jsx
function useChatRoom({ serverUrl, roomId, onMessage }) {
  const onMsg = useEffectEvent(onMessage);          // React 19.2+; avoids reconnect when the handler identity changes
  useEffect(() => {
    const c = createConnection(serverUrl, roomId);
    c.on("message", m => onMsg(m)); c.connect();
    return () => c.disconnect();
  }, [serverUrl, roomId]);
}
```
Do not use `useEffectEvent` to avoid listing real dependencies; only use it for logic that is genuinely an event fired from an Effect.

## 5. Avoid lifecycle hooks
`useMount(fn)` / `useEffectOnce` hide dependencies from the linter and lead to stale bugs. Write hooks for a purpose (`useWindowSize`, `useDebouncedValue`, `useIntersection`), not a lifecycle.

## 6. Return shape
Tuple `[value, setValue]` when there are two things the caller will rename; an object when there are more. Memoise returned functions (`useCallback`) if callers will put them in dependency arrays.

## 7. Test
```jsx
const { result, rerender } = renderHook(({ v }) => useDebouncedValue(v, 300), { initialProps: { v: "a" } });
```
`renderHook` from `@testing-library/react`; use fake timers for time-based hooks.

## Verify
- [ ] ESLint hooks rules pass with zero disables.
- [ ] Each custom hook has a name that says what it does and a test.
- [ ] Hook works with SSR (no `window` access during render without a server snapshot).

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20) and the Testing Library docs. Confirmed: hook names start with `use` and a capital letter and a function that uses no hook should not be named as one; custom hooks share logic, not state; the guidance to avoid custom lifecycle hooks; `useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot?)` with a server snapshot used during server rendering and hydration; `useEffectEvent` shipped in React 19.2 and must only be called from Effects; `renderHook` with `initialProps` exists in React Testing Library. Removed the pre-19.2 ref workaround, which the docs do not give.

Method: documentation only; no commands were run.
