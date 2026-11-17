---
id: computing-software.web-development.htmx.htmx-pattern-view-transitions
name: htmx-pattern-view-transitions
category: computing-software
field: web-development
product: htmx
tags: [htmx, view-transitions, hx-swap, animation, css, view-transition-name]
level: practitioner
status: docs-checked
description: "Use the browser View Transitions API with htmx via hx-swap 'innerHTML transition:true', a view-transition-name class, and ::view-transition-old/new keyframes."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/essays/view-transitions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: animate a whole content swap (old slides out, new slides in) using the View Transition API, with two small additions: CSS and an `hx-swap` modifier.

htmx wraps its normal swap around the browser's `document.startViewTransition(...)` API. You opt in per swap by adding `transition:true` to `hx-swap`. The essay says this is available as of htmx 1.9.0.

1. Define the animation in CSS and tie it to an element through `view-transition-name`:

```html
<style>
  @keyframes fade-in { from { opacity: 0; } }
  @keyframes fade-out { to { opacity: 0; } }
  @keyframes slide-from-right { from { transform: translateX(90px); } }
  @keyframes slide-to-left { to { transform: translateX(-90px); } }

  .slide-it { view-transition-name: slide-it; }

  ::view-transition-old(slide-it) {
    animation: 180ms cubic-bezier(0.4, 0, 1, 1) both fade-out,
               600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-to-left;
  }
  ::view-transition-new(slide-it) {
    animation: 420ms cubic-bezier(0, 0, 0.2, 1) 90ms both fade-in,
               600ms cubic-bezier(0.4, 0, 0.2, 1) both slide-from-right;
  }
</style>
```

2. Mark the element that will be mutated and opt in on the control:

```html
<div class="slide-it">
  <h1>Initial Content</h1>
  <button hx-get="/new-content" hx-swap="innerHTML transition:true" hx-target="closest div">
    Swap It!
  </button>
</div>
```

The returned fragment should include its own `hx-swap="... transition:true"` button if you want to animate back (the demo's "Restore It!" button does).

Gotchas
- The essay (April 2023) says the API had only just shipped in Chrome 111+ and that other browsers work fine but get no animation. Check current browser support before relying on it.
- The essay contrasts this with htmx's CSS-transition swapping model (htmx-pattern-css-animations), which settles attributes on elements present in both old and new content; View Transitions animate the whole DOM change.

## Checked

2026-11-07. Confirmed against the htmx "View Transitions" essay (htmx 1.9.0, `transition:true`, the `@keyframes` and `::view-transition-old/new` CSS, `view-transition-name`, the button markup, Chrome 111+ note, demo "Restore It!" button). Removed an unsourced DOM-presence claim and the invented Verify step; dropped the animations page from `sources` (not needed for the claims kept).
Method: documentation only; no commands were run.
