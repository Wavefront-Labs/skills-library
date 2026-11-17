---
id: computing-software.web-development.frontend-development.target-pseudo-class-and-scroll-margin
name: target-pseudo-class-and-scroll-margin
category: computing-software
field: web-development
product: frontend-development
tags: [target-pseudo-class, scroll-margin, anchor-links, fragment-navigation, css-selectors]
level: practitioner
status: docs-checked
description: "In-page anchor links done right: :target highlighting, scroll-margin-top under sticky headers, smooth scroll with reduced motion, focus management, and text fragments."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:target
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-margin
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/scroll-padding
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/::target-text
  - https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment/Text_fragments
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# :target and scroll-margin for anchor links

## 1. Sticky header offset
```css
:root { --header-h: 4rem; }
.site-header { position: sticky; top: 0; height: var(--header-h); }
:target, h2[id], h3[id] { scroll-margin-top: calc(var(--header-h) + 1rem); }
html { scroll-padding-top: calc(var(--header-h) + 1rem); }   /* alternative: on the scroll container */
```
Without it, the heading lands hidden under the sticky header. `scroll-padding` on the scroll container is the alternative (MDN uses it to stop content hiding under a fixed header).

## 2. Highlight the target
```css
:target { animation: flash 1.5s ease-out; }
@keyframes flash { from { background: color-mix(in oklch, gold 60%, transparent); } }
section:has(:target) { outline: 2px solid var(--accent); }
```
`:target` matches the element whose `id` equals the URL fragment; changes on hash navigation and back/forward.

## 3. Smooth scrolling
```css
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
```
Scoping smooth scrolling to `prefers-reduced-motion: no-preference` respects user settings.

## 4. Focus
For skip links and SPA-rendered anchors, add `tabindex="-1"` to the target and call `.focus()` so screen readers announce it.

## 5. SPAs and dynamic content
- Client routers often break fragments: after rendering, `document.getElementById(decodeURIComponent(location.hash.slice(1)))?.scrollIntoView()`.
- `:target` is set at document load and by history traversal (`back()`, `forward()`, `go()`), but not by `history.pushState()` or `replaceState()`.
- Ids must be unique and stable (slugify headings deterministically) so shared links survive content edits.

## 6. Text fragments
`https://example.com/page#:~:text=exact%20phrase` scrolls to and highlights text without ids. Style the match with `::target-text` (Chrome 89, Firefox 131, Safari 18.2).

## Verify
- [ ] Deep links land with the heading fully visible below the sticky header; target highlighted; reduced-motion users get instant jumps; SPA reload with a hash scrolls correctly.

## Checked

Checked 2026-10-26 against current documentation. MDN `:target` (set at document load and by `back()`/`forward()`/`go()`, not by `pushState()`/`replaceState()`), `scroll-padding` fixed-header example, `scroll-margin`, and `::target-text` support (Chrome 89, Firefox 131, Safari 18.2). Removed unconfirmed Ctrl+F smooth-scroll, focus-starting-point and Navigation API claims.

Method: documentation only; no commands were run.
