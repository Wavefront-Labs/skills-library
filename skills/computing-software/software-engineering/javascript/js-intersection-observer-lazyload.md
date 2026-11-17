---
id: computing-software.software-engineering.javascript.js-intersection-observer-lazyload
name: js-intersection-observer-lazyload
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, intersectionobserver-lazy, js-observers]
level: practitioner
status: docs-checked
description: "Lazy-load media with IntersectionObserver using rootMargin, thresholds, isIntersecting, unobserve and disconnect."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API", "https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# IntersectionObserver lazy loading

- The Intersection Observer API asynchronously reports how a target intersects an ancestor or the viewport; lazy-loading images or content while scrolling is a listed use case.
- `new IntersectionObserver(callback, { root, rootMargin, threshold })`. The callback gets `IntersectionObserverEntry` objects for targets whose visibility crossed a threshold in either direction. `entry.isIntersecting` tells you whether the target is at least partially intersecting, so check it to separate "entered" from "left".
- Positive `rootMargin` grows the clipping rectangle so targets intersect before they become visible, which starts loads slightly ahead of the viewport. The default threshold `0` fires on the `isIntersecting` change; `threshold: [0, 0.25, 0.5, 0.75, 1]` reports each 25% crossing.
- Load the resource in the callback, then `observer.unobserve(target)` so it is not reported again; call `observer.disconnect()` when finished or on teardown.
- Native alternative: images support `loading="lazy"` (`HTMLImageElement.loading` takes `eager` or `lazy`).

Self-check: only images near the viewport are requested in the Network panel, and each is unobserved after loading.

## Checked

2026-11-03. Confirmed on MDN: Intersection Observer API (asynchronous observation, lazy-load use case, rootMargin, threshold arrays, `isIntersecting`, `unobserve`, `disconnect`, the `data-src` lazy image example), HTMLImageElement.loading (`eager`/`lazy`). Removed: `content-visibility: auto`, the infinite-scroll sentinel and loading-flag advice, and the zero-area-target remark, none on a page read.
Method: documentation only; no commands were run.
