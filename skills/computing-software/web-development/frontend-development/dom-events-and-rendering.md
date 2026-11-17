---
id: computing-software.web-development.frontend-development.dom-events-and-rendering
name: dom-events-and-rendering
category: computing-software
field: web-development
product: frontend-development
tags: [frontend, front-end, dom, javascript, vanilla-js, events, event-delegation, addeventlistener, passive-listeners, event-bubbling, closest, layout-thrashing, forced-reflow, forced-synchronous-layout, requestanimationframe, batching, documentfragment, abortcontroller, abortsignal, fetch, cleanup, memory-leaks, progressive-enhancement, feature-detection, supports, intersectionobserver, resizeobserver, rendering-performance, web-development]
level: practitioner
status: docs-checked
description: "Framework-free DOM work: event delegation, passive listeners, avoiding layout thrashing, requestAnimationFrame, batched writes, AbortController cleanup, feature detection."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener
  - https://developer.mozilla.org/en-US/docs/Web/API/AbortController
  - https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
  - https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/focusin_event
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DOM events and rendering — few listeners, batched writes, clean teardown

**Goal:** wire up interactive UI with plain DOM APIs (or understand what your framework
does underneath) so it stays smooth at 60fps, leaks nothing, and still works when
JavaScript or a feature is missing.

## 1. Event delegation
One listener on a stable ancestor instead of one per row — works for rows added later.
```js
list.addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-action]');
  if (!btn || !list.contains(btn)) return;
  const id = btn.closest('li').dataset.id;
  if (btn.dataset.action === 'delete') removeItem(id);
});
```
- Use `closest()` because `e.target` may be an icon `<svg>` inside the button.
- `focus`/`blur` don't bubble; delegate `focusin`/`focusout` instead.
- `mouseenter`/`mouseleave` don't bubble; use `pointerover`/`pointerout` or per-element listeners.
- `stopPropagation()` breaks every delegated listener above you (analytics, menus that close on outside click) — avoid it.

## 2. Listener options
```js
el.addEventListener('touchstart', onTouch, { passive: true });  // can't preventDefault → scrolling never waits
el.addEventListener('click', onOnce, { once: true });
```
Per MDN, `wheel`, `mousewheel`, `touchstart` and `touchmove` listeners default to passive on some top-level targets; on other elements, declare it. If you genuinely need
`preventDefault()` on touch (custom gestures), set `passive: false` and use CSS `touch-action`
where possible instead.

## 3. Layout thrashing (forced synchronous layout)
Reading a geometry property (`offsetHeight`, `getBoundingClientRect()`, `scrollTop`,
`getComputedStyle`) after a style write forces the browser to recalculate layout right
now. In a loop that is N layouts per frame.
```js
// ✘ read/write interleaved: layout every iteration
for (const el of items) el.style.width = el.parentNode.offsetWidth / 2 + 'px';
// ✔ read everything, then write everything
const widths = items.map(el => el.parentNode.offsetWidth);
items.forEach((el, i) => { el.style.width = widths[i] / 2 + 'px'; });
```
The DevTools Performance panel flags forced reflows; use it to find the offending line.

## 4. Schedule visual work
- **`requestAnimationFrame`** for anything visual tied to scroll, pointer moves or animation: it runs once just before paint, so coalesce many events into one update.
```js
let queued = false, lastY = 0;
addEventListener('scroll', () => {
  lastY = scrollY;
  if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; render(lastY); }); }
}, { passive: true });
```
- Animate `transform` and `opacity` (compositor only); animating `top`, `width`, `height` triggers layout each frame.
- Build many nodes off-document (`DocumentFragment`, or one `replaceChildren(...nodes)`) and insert once.
- Replace scroll-position polling with `IntersectionObserver` (lazy loading, "seen" tracking) and window resize with `ResizeObserver` per element.
- Break long tasks into chunks so input isn't blocked: `await scheduler.yield()` where supported (check MDN's compatibility table), else `await new Promise(r => setTimeout(r))`.
- `content-visibility: auto` with `contain-intrinsic-size` skips rendering off-screen sections of long pages.

## 5. Cleanup with AbortController
One signal tears down listeners and requests together — the vanilla equivalent of an effect cleanup.
```js
function mount(root) {
  const ctrl = new AbortController();
  const { signal } = ctrl;
  root.addEventListener('input', onInput, { signal });
  window.addEventListener('resize', onResize, { signal });
  fetch('/api/data', { signal }).then(r => r.json()).then(render)
    .catch(err => { if (err.name !== 'AbortError') throw err; });
  return () => ctrl.abort();     // removes listeners AND cancels the fetch
}
```
Use it for search-as-you-type: abort the previous request before starting the next, so a
slow early response can't overwrite a newer one. `AbortSignal.timeout(5000)` gives a fetch
deadline; `AbortSignal.any([a, b])` combines signals.

## 6. Progressive enhancement and feature detection
Start from HTML that works: a real `<form action method>` and real `<a href>`. JavaScript
then intercepts and enhances. Detect features, not browsers:
```js
if ('IntersectionObserver' in window) lazyLoad(); else loadAllImages();
if (CSS.supports('selector(:has(a))')) document.documentElement.classList.add('has-has');
```
```css
@supports (container-type: inline-size) { .card-list { container-type: inline-size; } }
```
Avoid user-agent sniffing.

## Checked

2026-11-01. Confirmed in MDN source: `addEventListener` options `passive`, `once`, `signal`; `focusin` bubbles while `focus` does not; `AbortSignal.timeout()` and `AbortSignal.any()`; `scheduler.yield()` exists. Removed: DevTools colour description, 50 ms figure, UA-freezing claim.

Method: documentation only; no commands were run.

## Verify
- [ ] Lists use one delegated listener; adding rows dynamically needs no new binding.
- [ ] Performance panel shows no "Forced reflow" warnings during scroll or typing.
- [ ] Scroll/pointer handlers are passive and coalesced with `requestAnimationFrame`.
- [ ] Unmounting a widget aborts its fetches and removes its listeners (heap snapshot shows no detached nodes growing).
- [ ] Core flows (submit, navigate) still work with JavaScript disabled or a failed script.
