---
id: computing-software.web-development.frontend-development.unsaved-changes-guards
name: unsaved-changes-guards
category: computing-software
field: web-development
product: frontend-development
tags: [beforeunload, unsaved-changes-guard, navigation-blocking, useblocker, onbeforerouteleave, forms]
level: practitioner
status: docs-checked
description: "Warning users before losing unsaved work: beforeunload done right, in-app route blocking (React Router useBlocker, Vue Router, Navigation API) and autosave alternatives."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/beforeunload_event
  - https://reactrouter.com/api/hooks/useBlocker
  - https://router.vuejs.org/guide/advanced/navigation-guards.html#In-Component-Guards
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unsaved-changes guards

## 1. Tab close / reload / external navigation
```js
function onBeforeUnload(e) { e.preventDefault(); e.returnValue = ""; }   // returnValue for older browsers
function setDirty(dirty) {
  dirty ? addEventListener("beforeunload", onBeforeUnload) : removeEventListener("beforeunload", onBeforeUnload);
}
```
- Add the listener **only while dirty**, and remove it once saved.
- Do not rely on the prompt alone: autosave drafts.

## 2. In-app navigation
`beforeunload` does not fire for client-side route changes.
- React Router (data routers):
```jsx
const blocker = useBlocker(({ currentLocation, nextLocation }) => dirty && currentLocation.pathname !== nextLocation.pathname);
{blocker.state === "blocked" && <ConfirmDialog onStay={blocker.reset} onLeave={blocker.proceed} />}
```
- Vue Router: `onBeforeRouteLeave(() => !dirty.value || confirm("Discard changes?"))`.

## 3. Better UX than blocking
- Autosave to the server or `localStorage` with "Restored your draft" on return.
- Disable the guard after a successful save **before** navigating away.
- Use an accessible custom dialog for in-app confirmation (focus trapped, Escape = stay).

## Verify
- [ ] Edit a form, press reload: prompt shows; save, then reload: no prompt.
- [ ] Clicking an in-app link with unsaved edits shows the dialog; Stay keeps the data.

## Checked
2026-10-28 Confirmed on MDN (beforeunload: preventDefault, returnValue for legacy cases), React Router useBlocker (blocker state, proceed, reset; does not handle hard reloads) and Vue Router (onBeforeRouteLeave). Removed: custom-message, sticky-activation and back/forward cache claims, Safari behaviour, Navigation API and Next.js notes (not on fetched pages).
Method: documentation only; no commands were run.
