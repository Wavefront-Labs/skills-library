---
id: computing-software.web-development.frontend-development.common-flexbox-patterns
name: common-flexbox-patterns
category: computing-software
field: web-development
product: frontend-development
tags: [flexbox, sticky-footer, flex-patterns, media-object, holy-grail, css]
level: practitioner
status: docs-checked
description: "Implementing common flexbox layout patterns: sticky footer, media object, holy grail with sidebars, split navigation, input groups, and equal-height cards with aligned actions."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Flexible_box_layout/Use_cases
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Common flexbox patterns

## 1. Sticky footer
```css
body { min-height: 100svh; display: flex; flex-direction: column; margin: 0; }
main { flex: 1; }
```
Footer sits at the bottom on short pages and after content on long ones. Grid alternative: `body { display: grid; grid-template-rows: auto 1fr auto; }`.

## 2. Media object (image + text)
```css
.media { display: flex; gap: 1rem; align-items: flex-start; }
.media > img { flex: none; inline-size: 4rem; block-size: 4rem; object-fit: cover; border-radius: 50%; }
.media > .body { flex: 1; min-width: 0; }
```

## 3. Holy grail
```css
.page { display: flex; flex-wrap: wrap; gap: 1.5rem; }
.page > nav, .page > aside { flex: 1 1 12rem; }
.page > main { flex: 999 1 30rem; min-width: 0; }   /* main takes the space; sidebars wrap below when narrow */
```
For strict 2D placement (header/footer spanning, named areas), use grid instead.

## 4. Split navigation
```css
.topbar { display: flex; align-items: center; gap: 1rem; }
.topbar .spacer, .topbar .push { margin-inline-start: auto; }
```

## 5. Input group
```css
.input-group { display: flex; }
.input-group input { flex: 1; min-width: 0; }
.input-group button { flex: none; }
```

## 6. Cards with aligned actions
```css
.cards { display: flex; flex-wrap: wrap; gap: 1rem; }
.card { flex: 1 1 18rem; display: flex; flex-direction: column; }
.card .actions { margin-block-start: auto; }
```

## Rules
Prefer `gap` over margins, `min-width: 0` on growing text containers, and keep source order meaningful.

## Verify
Test each pattern at 320px, 768px and wide with long and short content; no overflow, footer stays down.

## Checked
2026-10-26. MDN flexbox use cases page (main, 2026-10-26): confirmed the media object, split navigation with auto margin, card layout pushing the footer down, and form control (input group) patterns. The sticky-footer and holy-grail snippets use only standard flex and grid shorthand and were not tied to a documentation page; removed the unread third-party sources.
Method: documentation only; no commands were run.
