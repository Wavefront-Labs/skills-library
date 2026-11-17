---
id: computing-software.web-development.web-performance.inp-presentation-delay-and-dom-size
name: inp-presentation-delay-and-dom-size
category: computing-software
field: web-development
product: web-performance
tags: [inp, presentation-delay, dom-size, rendering, content-visibility, core-web-vitals, dom-size-reduction]
level: practitioner
status: docs-checked
description: "Cutting INP presentation delay: large DOMs, expensive style and layout after updates, content-visibility, virtualised lists, and avoiding layout thrashing in handlers."
sources:
  - https://web.dev/articles/optimize-inp#presentation_delay
  - https://web.dev/articles/dom-size-and-interactivity
  - https://developer.mozilla.org/en-US/docs/Web/CSS/content-visibility
  - https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# INP presentation delay and DOM size

**Presentation delay** = from the end of event handlers until the next frame is painted: style recalculation, layout, paint and compositing triggered by the update, plus any rAF callbacks.

## 1. Diagnose
Performance panel: after the interaction's event handler, look for large purple (Recalculate Style, Layout) and green (Paint) blocks. Hover to see elements affected.

## 2. DOM size
- Lighthouse flags DOM size as excessive above 1,400 nodes and begins warning at 800; costs scale with nodes affected by a change.
- Common offenders: rendering all 5,000 table rows, mega menus duplicated for mobile and desktop, hidden tabs/modals fully rendered, SVG icon sprites inlined repeatedly, rich text editors.
- Fixes: virtualise long lists, paginate, render hidden content lazily, remove duplicate desktop/mobile markup.

## 3. content-visibility
```css
.feed-item { content-visibility: auto; contain-intrinsic-size: auto 400px; }
```
Skips rendering of off-screen sections until needed (Baseline 2024). `contain-intrinsic-size` reserves estimated space to avoid scrollbar jumps (`auto` remembers the real size after first render). Don't apply to above-the-fold content.

## 4. Cheaper style and layout
- Scope changes: toggling a class on `body` restyles everything; toggle on the smallest container.
- Animate `transform`/`opacity` only.
- Avoid read-after-write layout thrashing in handlers (`offsetHeight` after style writes) - batch reads, then writes.

## 5. Give the user feedback first
Update the minimal visible state (pressed button, spinner) and yield before heavy re-render, so the next paint happens fast (see the web.dev INP presentation-delay guidance on yielding).

## Verify
Interaction's presentation delay in DevTools shrinks; DOM node count (`document.querySelectorAll("*").length`) reduced on heavy pages.

## Checked

2026-10-28. Confirmed from web.dev DOM size and interactivity (Lighthouse flags more than 1,400 nodes, warns from 800), MDN `content-visibility` (Baseline 2024, `contain-intrinsic-size` with `auto`) and web.dev on layout thrashing. Removed (not found): LoAF field names, the 32-level depth claim, library names, `:has()` and `contain` advice, `scheduler.yield()` and `startTransition` specifics, the 50 ms target.

Method: documentation only; no commands were run.
