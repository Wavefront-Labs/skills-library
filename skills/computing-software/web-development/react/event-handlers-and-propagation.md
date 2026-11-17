---
id: computing-software.web-development.react.event-handlers-and-propagation
name: event-handlers-and-propagation
category: computing-software
field: web-development
product: react
tags: [react, react-event-handlers, synthetic-events, event-propagation, stoppropagation, preventdefault, web-development]
level: practitioner
status: verified
description: "Writing React event handlers correctly: passing vs calling, propagation and capture, preventDefault, handler props naming and side effects in handlers."
sources:
  - https://react.dev/learn/responding-to-events
  - https://react.dev/reference/react-dom/components/common#react-event-object
  - https://legacy.reactjs.org/blog/2020/08/10/react-v17-rc.html#changes-to-event-delegation
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event handlers and propagation in React

**Goal:** handlers that fire once, at the right element, with side effects where they belong.

## 1. Pass, don't call
```jsx
<button onClick={handleClick}>        // correct
<button onClick={() => remove(id)}>   // correct, needs an argument
<button onClick={handleClick()}>      // bug: runs during render, every render
```

## 2. Handler props
Name props by meaning, `onX`; name handlers `handleX`:
```jsx
function Toolbar({ onPlay, onUpload }) {
  return <><Button onClick={onPlay}>Play</Button><Button onClick={onUpload}>Upload</Button></>;
}
```
Custom components only fire what they wire: `<Button onClick>` does nothing unless `Button` passes it to a DOM element.

## 3. Propagation
All events propagate in React except `onScroll`, which only fires on the tag it is attached to (react.dev, checked: a bubbling native scroll never reached the outer `onScroll`). React attaches listeners at the root container (since 17), but propagation semantics mirror the DOM.
```jsx
<div onClick={() => setOpen(false)}>
  <button onClick={(e) => { e.stopPropagation(); save(); }}>Save</button>
</div>
```
- Prefer passing a handler down over `stopPropagation`; stopping propagation hides events from analytics and outer-close logic.
- Capture phase: `onClickCapture` runs on the way down - use for logging that must see every click.
- `e.preventDefault()` stops browser defaults (form submit reload, link navigation). It's not the same as stopping propagation.

## 4. Event object
React passes a synthetic event with the standard interface; `e.nativeEvent` gives the DOM event. Since React 17 there is no event pooling, so reading `e.target` in an async callback is fine.

## 5. Side effects belong in handlers
Sending a request because the user clicked = handler, not an effect watching a `submitted` flag. Handlers don't need to be pure; render does.

## 6. Native listeners
For `window`/`document` events, add in an effect with cleanup:
```jsx
useEffect(() => {
  const onKey = (e) => e.key === "Escape" && onClose();
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
}, [onClose]);
```
Passive listeners: React registers `touchstart`, `touchmove` and `wheel` as passive (checked by spying on `addEventListener`), so `preventDefault()` inside `onWheel` does nothing - attach a native non-passive listener via a ref when you need it.

## Verify
- [ ] No `onClick={fn()}` patterns: `grep -rnE "on[A-Z]\w*=\{\w+\(\)\}" src`.
- [ ] Clicking a nested control fires the intended handler only once (console log both levels).
- [ ] Forms call `preventDefault` or use a form action.
