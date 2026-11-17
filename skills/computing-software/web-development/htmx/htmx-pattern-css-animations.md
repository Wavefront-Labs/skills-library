---
id: computing-software.web-development.htmx.htmx-pattern-css-animations
name: htmx-pattern-css-animations
category: computing-software
field: web-development
product: htmx
tags: [htmx, animation, css-transitions, htmx-swapping, htmx-settling, htmx-added, htmx-request]
level: practitioner
status: docs-checked
description: "Animate htmx swaps with plain CSS: stable ids for transitions, htmx-swapping with swap:1s for fade-out, htmx-added with settle:1s for fade-in, htmx-request for in-flight."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/examples/animations.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: smooth transitions on swapped content using only CSS and htmx's swap lifecycle classes.

Lifecycle (docs.md "Request Order of Operations"): `htmx-request` is applied when the request starts; on response the target gets `htmx-swapping`; after the optional swap delay the swap happens, `htmx-swapping` is removed, `htmx-added` goes on each new piece of content and `htmx-settling` on the target; after the settle delay (default 20 ms) both are removed.

1. Keep the id stable. If the `id` of an element is kept stable, htmx swaps it in such a way that CSS transitions can be written between the old version and the new one (colour throb):

```html
<style>.smooth { transition: all 1s ease-in; }</style>
<div id="color-demo" class="smooth" style="color:red"
     hx-get="/colors" hx-swap="outerHTML" hx-trigger="every 1s">Color Swap Demo</div>
```
The server returns the same div with `style="color:blue"` and so on.

2. Fade out on removal: extend the swap phase so the CSS can finish.

```html
<style>.fade-me-out.htmx-swapping { opacity: 0; transition: opacity 1s ease-out; }</style>
<button class="fade-me-out" hx-delete="/fade_out_demo" hx-swap="outerHTML swap:1s">Fade Me Out</button>
```

3. Fade in on addition using the settle phase:

```html
<style>
#fade-me-in.htmx-added { opacity: 0; }
#fade-me-in { opacity: 1; transition: opacity 1s ease-out; }
</style>
<button id="fade-me-in" hx-post="/fade_in_demo" hx-swap="outerHTML settle:1s">Fade Me In</button>
```
You can also write transitions against the target using `htmx-settling`.

4. In-flight feedback with `htmx-request`:

```css
form.htmx-request { opacity: .5; transition: opacity 300ms linear; }
```

5. The class-tools extension can toggle classes on a timer, e.g. `<div class="demo" classes="toggle faded:1s">`. Set the toggle time slightly longer than the transition time (900 ms transition, 1 s toggle) to avoid flicker from interrupted transitions.

Related: htmx-pattern-view-transitions, htmx-pattern-progress-bar.

## Checked

2026-11-07. Confirmed on examples/animations.md (stable id, fade out with `swap:1s`, fade in with `settle:1s`, `htmx-request`, class-tools example and timing note) and docs.md (Request Order of Operations, default settle delay 20ms). The two related skills named are other library skills.
Fixed: the stable-id sentence now follows the page wording. Removed the invented Verify step.
Method: documentation only; no commands were run.
