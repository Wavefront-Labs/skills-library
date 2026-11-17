---
id: computing-software.web-development.tailwind-css.scroll-driven-animations
name: scroll-driven-animations
category: computing-software
field: web-development
product: tailwind-css
tags: [css-animations, css-transitions, scroll-driven-animations, scroll-timeline, view-timeline, animation-timeline, animation-range, reading-progress]
level: practitioner
status: verified
description: "Building scroll-linked effects in pure CSS with animation-timeline scroll() and view(), animation-range, progressive enhancement and reduced-motion handling."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations
  - https://developer.chrome.com/docs/css-ui/scroll-driven-animations
  - https://scroll-driven-animations.style/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scroll-driven animations

**Goal:** progress bars, reveal-on-scroll and parallax effects without scroll listeners, running off the main thread.

## 1. Scroll progress timeline
```css
@keyframes grow { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.reading-progress {
  position: fixed; inset: 0 0 auto 0; height: 4px; transform-origin: left;
  animation: grow linear both;
  animation-timeline: scroll(root block);     /* progress of the document scroller */
}
```
`scroll(<scroller> <axis>)`: scroller = `nearest` (default) | `root` | `self`.

## 2. View progress timeline (element entering/leaving)
```css
@keyframes reveal { from { opacity: 0; transform: translateY(2rem); } to { opacity: 1; transform: none; } }
.reveal {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;      /* start as it enters, finish when 30% through */
}
```
Ranges: `cover`, `contain`, `entry`, `exit`, `entry-crossing`, `exit-crossing` with percentages/lengths.

## 3. Rules
- Set `animation-timeline` **after** the `animation` shorthand (the shorthand resets it to `auto`).
- Duration is ignored for scroll timelines (use `linear` easing for 1:1 mapping; `auto` duration).
- Named timelines (`scroll-timeline-name`, `view-timeline-name` + `timeline-scope`) let another element animate based on a different scroller.
- Animate transform/opacity to stay on the compositor.

## 4. Support and enhancement
Chromium 115+ and Safari 26; Firefox behind a flag at time of writing - check current support. Wrap in a feature query so unsupported browsers show the final state:
```css
@supports (animation-timeline: view()) { .reveal { animation: reveal linear both; animation-timeline: view(); } }
```
A JS polyfill exists (flackr/scroll-timeline) but costs main-thread work.

## 5. Motion sensitivity
Parallax and scroll-zoom are classic vestibular triggers - put scroll-driven effects inside `@media (prefers-reduced-motion: no-preference)`.

## Verify
- [ ] Effects track scroll smoothly with CPU throttling (compositor-driven).
- [ ] Content fully visible in browsers without support.
- [ ] Disabled under reduced motion.
