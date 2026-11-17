---
id: computing-software.web-development.react.portals-and-root-apis
name: portals-and-root-apis
category: computing-software
field: web-development
product: react
tags: [react, portals, createportal, createroot, hydrateroot, modals, react-dom-client, web-development]
level: practitioner
status: verified
description: "Rendering outside the parent DOM with createPortal (modals, tooltips, toasts) and mounting apps with createRoot/hydrateRoot, including hydration options."
sources:
  - https://react.dev/reference/react-dom/createPortal
  - https://react.dev/reference/react-dom/client/createRoot
  - https://react.dev/reference/react-dom/client/hydrateRoot
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/dialog
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Portals and createRoot / hydrateRoot

**Goal:** overlays that escape `overflow: hidden`/stacking contexts, and correct root mounting for client and SSR apps.

## 1. createPortal
```jsx
import { createPortal } from "react-dom";
function Modal({ open, onClose, children }) {
  if (!open) return null;
  return createPortal(
    <div role="dialog" aria-modal="true" aria-labelledby="modal-title" className="modal">{children}</div>,
    document.body
  );
}
```
- DOM moves; the **React tree doesn't**: context works and events bubble to React ancestors (a click in the portal triggers a parent `onClick`). Stop propagation or check `e.currentTarget` if that's unwanted.
- SSR: `document` doesn't exist on the server. Render portals only after mount (`useEffect` sets a `mounted` flag) or into a node that exists.

## 2. Consider native first
`<dialog>` with `showModal()` renders in the top layer (no z-index wars), makes the rest of the page inert, and closes on Escape (MDN: the `cancel` event fires on Escape). The `popover` attribute handles non-modal popups. Use a portal when you need full control or wider support.

## 3. Modal accessibility checklist
Focus moves into the dialog and returns to the trigger on close, Tab is trapped, Escape closes, background is `inert`, title is labelled.

## 4. createRoot (client-only apps)
```jsx
import { createRoot } from "react-dom/client";
const root = createRoot(document.getElementById("root"), {
  onUncaughtError: (e) => report(e),          // React 19
  identifierPrefix: "app-",                    // for multiple roots using useId
});
root.render(<App />);
// root.unmount() when embedding in a non-React host that removes the node
```
Replaces legacy `ReactDOM.render` (removed in React 19: `render`, `hydrate`, `findDOMNode` and `unmountComponentAtNode` are all `undefined` on `react-dom` 19.3.1). Enables concurrent features and automatic batching.

## 5. hydrateRoot (SSR)
```jsx
import { hydrateRoot } from "react-dom/client";
hydrateRoot(document.getElementById("root"), <App />, { onRecoverableError: (e) => report(e) });
```
The client tree must render identical HTML to the server's first pass. Mismatches (dates, `Math.random`, `typeof window` branches, browser extensions editing the DOM) trigger recoverable errors and client re-render. Use `useId` for ids, and `suppressHydrationWarning` only on a single element with intentionally different text (timestamps).

## 6. Multiple roots / islands
Several `createRoot`s on one page are fine (micro-frontends, widgets in a CMS). A portal keeps the React tree (context and event bubbling) of the component that renders it, whichever DOM node it targets.

## Verify
- [ ] Modal is not clipped inside a scroll/overflow container.
- [ ] No hydration warnings in the console on SSR pages.
- [ ] Focus returns to the opening button after closing the modal.
