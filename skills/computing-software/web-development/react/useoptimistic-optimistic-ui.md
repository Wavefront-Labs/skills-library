---
id: computing-software.web-development.react.useoptimistic-optimistic-ui
name: useoptimistic-optimistic-ui
category: computing-software
field: web-development
product: react
tags: [react, useoptimistic, optimistic-ui, react-19, actions, rollback, web-development]
level: practitioner
status: docs-checked
description: "Showing optimistic updates with React 19 useOptimistic: reducer form, usage inside actions/transitions, automatic rollback on failure and pending markers."
sources:
  - https://react.dev/reference/react/useOptimistic
  - https://react.dev/reference/react/useTransition
  - https://tanstack.com/query/latest/docs/framework/react/guides/optimistic-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useOptimistic

**Goal:** the UI reflects a user's change instantly, then reconciles with the server result or reverts on failure.

## 1. Signature
```jsx
const [optimisticState, addOptimistic] = useOptimistic(state, (current, optimisticValue) => next);
```
`optimisticState` equals `state` except while an action/transition is pending, when the reducer's result is shown.

## 2. Example: sending a message
```jsx
function Thread({ messages, sendMessage }) {
  const [optimistic, addOptimistic] = useOptimistic(
    messages,
    (current, text) => [...current, { id: crypto.randomUUID(), text, sending: true }]
  );
  async function formAction(fd) {
    const text = fd.get("message");
    addOptimistic(text);
    await sendMessage(text);          // parent updates `messages` on success
  }
  return (
    <>
      {optimistic.map(m => <p key={m.id} style={{ opacity: m.sending ? 0.5 : 1 }}>{m.text}</p>)}
      <form action={formAction}><input name="message" /><button>Send</button></form>
    </>
  );
}
```

## 3. Rules
- Call `addOptimistic` inside an Action (a function passed to `startTransition` or a form `action`); outside one React shows a warning and the optimistic state renders only briefly.
- When the transition ends, the optimistic layer is dropped and the real `state` shows. If the server failed and `state` didn't change, the item disappears - that's the rollback. Show an error (toast, inline retry) so the user knows.
- The base `state` must be updated by the action's outcome (parent state, router refresh, `revalidatePath`) or the optimistic item vanishes even on success.

## 4. Marking pending items
Add `sending: true` in the reducer output and style it; never let users interact with pending items as if saved (e.g. disable edit/delete).

## 5. Without React 19 actions
TanStack Query's `onMutate` (snapshot, set cache, return context) / `onError` (restore) / `onSettled` (invalidate) gives the same with a cache; or simply render `mutation.variables` while `isPending`.

## Verify
- [ ] Throttle network: item appears immediately and dimmed.
- [ ] Force the server to fail: item disappears and an error is shown.
- [ ] Rapid multiple submissions all appear and reconcile in order.

## Checked

Checked 2026-10-25 against the React docs (useOptimistic and useTransition pages, react.dev repository last commit 2026-10-20) and the TanStack Query optimistic updates guide. Confirmed: `useOptimistic(value, reducer)` returns the optimistic state and a set function; the optimistic state equals `value` unless an Action is pending; the set function must be called inside an Action or React warns; when the base state changes during a pending Action the reducer re-runs; TanStack Query supports `onMutate`, `onError` and `onSettled` and rendering `variables` while `isPending`.

Method: documentation only; no commands were run.
