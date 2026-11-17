---
id: computing-software.web-development.frontend-development.view-transitions-api
name: view-transitions-api
category: computing-software
field: web-development
product: frontend-development
tags: [canvas-api, view-transitions, animation, spa, mpa, css]
level: practitioner
status: docs-checked
description: "Animating state and page changes with the View Transitions API: same-document startViewTransition, cross-document @view-transition, naming elements, and fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API
  - https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/view-transition-name
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@view-transition
  - https://drafts.csswg.org/css-view-transitions-2/
  - https://react.dev/reference/react/ViewTransition
  - https://github.com/mdn/browser-compat-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# View Transitions API

## 1. Same-document (SPA)
```js
function navigate(update) {
  if (!document.startViewTransition || matchMedia("(prefers-reduced-motion: reduce)").matches) return update();
  const t = document.startViewTransition(() => update());   // update may return a promise
  return t.finished;
}
```
The browser snapshots the old view, runs `update`, snapshots the new, and crossfades by default. Promises: `t.updateCallbackDone`, `t.ready` (pseudo-elements created, animate them via WAAPI), `t.finished`. `t.skipTransition()` to abort.

## 2. Shared-element morph
```css
.card-thumb { view-transition-name: hero; }           /* on old state */
.detail-hero { view-transition-name: hero; }          /* on new state */
::view-transition-old(hero), ::view-transition-new(hero) { animation-duration: .3s; }
::view-transition-group(root) { animation-duration: .2s; }
```
- Each `view-transition-name` must be unique in the document at snapshot time, or the transition is skipped with an error. For lists, set the name dynamically only on the clicked item, or use `view-transition-name: match-element` (newer).
- `view-transition-class` groups styling for many named elements.

## 3. Cross-document (MPA)
```css
@view-transition { navigation: auto; }   /* on both pages, same-origin navigations */
```
Chrome 126+ and Safari 18.2+ (no Firefox support in browser-compat-data). Events `pageswap` (old page) and `pagereveal` (new page) let you set names/types per navigation. `<link rel="expect">` blocks rendering until the critical content has been parsed, which keeps the first paint (and so the transition) consistent.

## 4. Pitfalls
- The old state is shown as a static image while the new state is a live, interactive region (MDN); keep durations short.
- Frameworks: React's `<ViewTransition>` is documented against Canary builds; with any framework the DOM update must happen inside the `startViewTransition` callback.
- Focus and scroll are not managed for you - still move focus after SPA navigation.
- Firefox: same-document supported from 144; always keep the no-API path working.

## Verify
Use the browser DevTools animation tools to slow the transition down. A duplicate `view-transition-name` makes the `ViewTransition.ready` promise reject (MDN), so watch for a skipped transition.

## Checked

Checked 2026-10-26 against current documentation. MDN View Transition API pages, `view-transition-name` (uniqueness, `match-element`), `@view-transition`, `pageswap`/`pagereveal`, `<link rel="expect">`, React ViewTransition reference (Canary builds) and browser-compat-data (same-document Chrome 111, Safari 18, Firefox 144; cross-document `@view-transition` Chrome 126, Safari 18.2, no Firefox; `match-element` Chrome 137, Safari 18.4, Firefox 144). Removed unconfirmed framework-integration, console-message and snapshot-stretching claims, and the 300 ms figure.

Method: documentation only; no commands were run.
