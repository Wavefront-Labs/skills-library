---
id: computing-software.web-development.tailwind-css.css-scope-rule
name: css-scope-rule
category: computing-software
field: web-development
product: tailwind-css
tags: [css-cascade, specificity, css-scope, at-scope, scoping-proximity, donut-scope, component-styles]
level: practitioner
status: verified
description: "Scoping styles to a DOM subtree with @scope: scope roots and limits (donut scope), proximity in the cascade, and when to prefer it over BEM or CSS Modules."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@scope
  - https://www.w3.org/TR/css-cascade-6/#scoped-styles
  - https://developer.chrome.com/docs/css-ui/at-scope
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @scope rules and proximity

**Goal:** component styles that only apply inside a component and stop at nested slots/other components, without long class names.

## 1. Basic scope
```css
@scope (.card) {
  :scope { border: 1px solid #ddd; border-radius: 8px; }   /* the root itself */
  img { aspect-ratio: 16/9; object-fit: cover; }            /* only imgs inside .card */
  .title { font-weight: 600; }
}
```
Selectors inside don't gain the root's specificity (unlike `.card img`), keeping them easy to override.

## 2. Donut scope (lower boundary)
```css
@scope (.card) to (.card__content) {
  a { color: inherit; text-decoration: none; }   /* links in card chrome, not in user content area */
}
```
The scope stops at elements matching the `to` selector - useful so a component's styles don't leak into slotted/nested content or nested components of the same type.

## 3. Proximity
When two scoped rules with equal specificity conflict, the one whose scope root is **closer** in the DOM wins - before source order is considered. Example: `.theme-light a` vs `.theme-dark a` nested themes: with `@scope (.theme-light)` and `@scope (.theme-dark)`, the nearest theme wins regardless of which rule comes later.

## 4. Inline scoped styles
```html
<div class="promo">
  <style>@scope { p { color: teal; } }</style>   <!-- scope root = parent element -->
  <p>Only this p is teal</p>
</div>
```

## 5. Support and alternatives
Browser data (MDN browser-compat-data): Chrome and Edge 118, Firefox 146, Safari 26.4; the web-features Baseline entry is "newly available" from 2026-03-24 (its Chrome figure is 143). Check Baseline for your audience. Behaviour checked in Chromium 156: `:scope` styling, the `to` donut boundary, nearest-root proximity (inner `.dark` beat outer `.light`) and the inline `@scope { }` form all worked as described, and `@scope (.card) { img }` lost to a plain `.x` class (no root specificity added). For wider support: CSS Modules / Vue `scoped` / Svelte (build-time class hashing) or BEM. `@scope` complements cascade layers: layers decide between sources, scope limits where rules apply.

## Verify
- [ ] Styles don't apply outside the scope root or past the `to` boundary (DevTools Styles shows `@scope` rules).
- [ ] Nested themes resolve by proximity.
- [ ] Fallback acceptable in unsupported browsers (feature query `@supports at-rule(@scope)` is not universal - test visually).
