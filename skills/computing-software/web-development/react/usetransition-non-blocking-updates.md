---
id: computing-software.web-development.react.usetransition-non-blocking-updates
name: usetransition-non-blocking-updates
category: computing-software
field: web-development
product: react
tags: [react, usetransition, starttransition, concurrent-rendering, pending-state, async-transitions, web-development]
level: practitioner
status: docs-checked
description: "Keeping React UIs responsive with useTransition/startTransition: marking non-urgent updates, isPending UI, async transitions in React 19 and limits."
sources:
  - https://react.dev/reference/react/useTransition
  - https://react.dev/reference/react/startTransition
  - https://react.dev/reference/react/Suspense
  - https://react.dev/blog/2024/12/05/react-19#actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useTransition and startTransition

**Goal:** expensive re-renders (tab switches, big lists, navigation) never block typing or clicking.

## 1. Mark the update as non-urgent
```jsx
const [isPending, startTransition] = useTransition();
function selectTab(next) {
  startTransition(() => setTab(next));
}
return <TabButton onClick={() => selectTab("posts")} dim={isPending} />;
```
React renders the new tab in the background; new urgent input interrupts it. The old UI stays visible (with `isPending`) instead of a blocked main thread or a Suspense fallback flashing.

## 2. Async transitions (React 19)
```jsx
startTransition(async () => {
  const err = await updateName(name);
  startTransition(() => { if (err) setError(err); else redirect("/me"); });
});
```
`isPending` stays true for the whole async function. State updates **after** an `await` need wrapping in another `startTransition` (a known limitation the React team plans to fix).

## 3. Rules
- Transitions are for **state updates**, not for controlled input values. `startTransition(() => setQuery(e.target.value))` makes typing laggy. Keep the input urgent and defer the expensive consumer (`useDeferredValue`) or transition a second state.
- The function passed runs synchronously; only `set` calls inside it are marked.
- Standalone `startTransition` (imported from `react`) when you have no component, e.g. in a store or router.

## 4. Suspense interplay
Navigations wrapped in transitions keep showing the current page rather than replacing already-revealed content with a fallback. Suspense-enabled routers are expected to wrap navigation updates in transitions by default.

## 5. It doesn't make code faster
Rendering still costs the same CPU. If a single render is very slow, also memoise, virtualise (`@tanstack/react-virtual`), or move work off the main thread.

## Verify
- [ ] With CPU throttled 6x, clicking another tab mid-render switches immediately.
- [ ] Pending state is visible (opacity/spinner) during slow transitions.
- [ ] No controlled input updates wrapped in `startTransition`.

## Checked

Checked 2026-10-25 against the React docs (useTransition, startTransition and Suspense pages, react.dev repository last commit 2026-10-20). Confirmed: `isPending` stays true until all Actions finish; async Actions are supported and state updates after an `await` must be wrapped in another `startTransition` (documented limitation); the callback runs immediately and only state updates scheduled synchronously inside it are marked; transitions cannot control text inputs and the two alternatives; a transition update that re-suspends already revealed content keeps showing it; Suspense-enabled routers are expected to wrap navigation in transitions. Removed the AsyncContext reference and the 500 ms figure.

Method: documentation only; no commands were run.
