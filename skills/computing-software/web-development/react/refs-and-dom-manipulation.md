---
id: computing-software.web-development.react.refs-and-dom-manipulation
name: refs-and-dom-manipulation
category: computing-software
field: web-development
product: react
tags: [react, forwardref, useimperativehandle, useref, ref-as-prop, ref-callback, dom-refs, focus-management, web-development]
level: practitioner
status: verified
description: "Accessing DOM nodes in React: useRef, ref as a prop in React 19 vs forwardRef, ref callbacks with cleanup, useImperativeHandle and safe DOM mutation."
sources:
  - https://react.dev/learn/manipulating-the-dom-with-refs
  - https://react.dev/reference/react/useImperativeHandle
  - https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop
  - https://react.dev/reference/react-dom/components/common#ref-callback
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manipulating the DOM with refs

**Goal:** use refs for focus, scroll, measurement and third-party widgets without fighting React.

## 1. Basic ref
```jsx
const inputRef = useRef(null);
<input ref={inputRef} />
<button onClick={() => inputRef.current.focus()}>Edit</button>
```
`ref.current` is null during render and set before layout effects run. Never read or write `ref.current` during render (except lazy init).

## 2. Passing refs to your components
React 19: `ref` is a regular prop on function components.
```jsx
function TextInput({ ref, ...props }) { return <input ref={ref} {...props} />; }
```
React 18 and earlier: wrap with `forwardRef((props, ref) => ...)`. `forwardRef` still works in 19; react.dev marks it deprecated ("will be deprecated in a future release").

## 3. Expose a narrow API
```jsx
function VideoPlayer({ ref, src }) {
  const video = useRef(null);
  useImperativeHandle(ref, () => ({
    play: () => video.current.play(),
    pause: () => video.current.pause(),
  }), []);
  return <video ref={video} src={src} />;
}
```
Parents get `play/pause`, not the whole DOM node. Use imperative handles for actions (focus, scroll, play) - not for things expressible as props (`isOpen`).

## 4. Lists of refs: ref callbacks
```jsx
const itemsRef = useRef(new Map());
{items.map(item => (
  <li key={item.id} ref={node => {
    itemsRef.current.set(item.id, node);
    return () => itemsRef.current.delete(item.id);   // React 19 cleanup
  }}>{item.name}</li>
))}
```
Pre-19 the callback gets `null` on unmount instead of running a cleanup (checked on 19.3.1: setup for both items, then both cleanups on unmount).

## 5. Safe DOM mutation
Fine: focus, scroll, measuring, selection, media playback, integrating non-React widgets in an element React leaves empty. Not fine: adding/removing nodes React manages - it will crash or desync on next update.

## 6. Timing
After `setState`, the DOM isn't updated yet. Scroll/focus after the commit: in an effect, or use `flushSync` in the handler.

## 7. Refs as instance variables
`useRef` also stores mutable values that don't trigger renders (interval ids, latest callback, previous value).

## Verify
- [ ] No `ref.current` reads in render bodies.
- [ ] Component library components accept `ref` (or `forwardRef`) and forward to the focusable element.
- [ ] Dialog open moves focus in; close returns focus to the trigger.
