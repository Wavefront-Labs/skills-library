---
id: computing-software.web-development.react.uselayouteffect-and-measuring-layout
name: uselayouteffect-and-measuring-layout
category: computing-software
field: web-development
product: react
tags: [react, uselayouteffect, layout-measurement, getboundingclientrect, resizeobserver, tooltips, ssr, web-development]
level: practitioner
status: docs-checked
description: "Measuring layout before paint with useLayoutEffect: tooltip positioning, avoiding flicker, SSR warnings, ResizeObserver and performance cost."
sources:
  - https://react.dev/reference/react/useLayoutEffect
  - https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
  - https://floating-ui.com/docs/react
  - https://developer.mozilla.org/en-US/docs/Web/CSS/anchor-name
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useLayoutEffect and measuring layout

**Goal:** position or size things from DOM measurements without a visible flicker.

## 1. When it's needed
`useEffect` runs after paint: measuring there and setting state shows one wrong frame (tooltip jumps). `useLayoutEffect` runs after DOM mutation but before paint, and state updates inside it are processed synchronously before the browser paints.

```jsx
function Tooltip({ targetRect, children }) {
  const ref = useRef(null);
  const [height, setHeight] = useState(0);
  useLayoutEffect(() => {
    setHeight(ref.current.getBoundingClientRect().height);
  }, []);
  const y = targetRect.top - height < 0 ? targetRect.bottom : targetRect.top - height;
  return <div ref={ref} style={{ position: "fixed", top: y, left: targetRect.left }}>{children}</div>;
}
```

## 2. Cost
It blocks paint. Keep it to read-measure-set; never fetch or do heavy work. Many layout effects across a list = jank.

## 3. SSR
Effects, layout effects included, only run on the client, and there is no layout information on the server, so the server HTML is rendered without measurements. Options from the React docs: use `useEffect` instead, mark the component client-only (a Suspense fallback is shown during server rendering), or render the layout-dependent content only after hydration using an `isMounted` state set in an Effect. Components that need layout, such as tooltips, usually open after a client interaction anyway.

## 4. Continuous measurement
Initial measure in a layout effect, then observe:
```jsx
useLayoutEffect(() => {
  const el = ref.current;
  const ro = new ResizeObserver(([e]) => setSize(e.contentRect));
  ro.observe(el);
  return () => ro.disconnect();
}, []);
```
Avoid reading layout in `scroll` handlers each frame; use IntersectionObserver or CSS where possible.

## 5. Don't build positioning engines
For tooltips/popovers/menus use Floating UI (`useFloating`, `autoUpdate`) or CSS anchor positioning (`anchor-name`, `position-anchor`) where supported - they handle flipping, collision and scroll containers.

## 6. Avoid layout thrash
Batch DOM reads before writes so the browser does not have to recompute layout between them.

## Verify
- [ ] With CPU throttled 6x, the tooltip never appears in the wrong place for a frame.
- [ ] Performance panel shows no long tasks from layout effects on scroll/resize.
- [ ] SSR page doesn't shift visibly when the measured value applies.

## Checked

Checked 2026-10-25 against the React docs (useLayoutEffect page, react.dev repository last commit 2026-10-20), MDN and the Floating UI docs. Confirmed: `useLayoutEffect` fires before the browser repaints and state updates scheduled inside it are processed before the repaint (it blocks painting); Effects only run on the client; the documented server-rendering options; `ResizeObserver` and `contentRect`; `useFloating` and `autoUpdate` exist in Floating UI; `anchor-name` and `position-anchor` are documented CSS properties on MDN. Removed the React 18/19 warning history and the `offsetHeight` forced-layout claim.

Method: documentation only; no commands were run.
