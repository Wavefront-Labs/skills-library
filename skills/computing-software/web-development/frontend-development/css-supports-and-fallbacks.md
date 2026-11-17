---
id: computing-software.web-development.frontend-development.css-supports-and-fallbacks
name: css-supports-and-fallbacks
category: computing-software
field: web-development
product: frontend-development
tags: [css-supports-query, css-fallbacks, feature-queries, css-supports-selector, progressive-enhancement, css]
level: practitioner
status: docs-checked
description: "Progressive enhancement in CSS: cascade fallbacks, @supports for properties/selectors/font tech, CSS.supports in JS, and the selector-list and var() traps."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@supports
  - https://developer.mozilla.org/en-US/docs/Web/API/CSS/supports_static
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Selectors/:is
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/var
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Syntax/Error_handling
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# @supports and CSS fallbacks

## 1. Cascade fallbacks (no query needed)
Browsers drop declarations they do not understand, so declare old then new:
```css
.hero { height: 100vh; height: 100dvh; }
.card { background: #6d28d9; background: oklch(50% 0.2 290); }
```

## 2. Feature queries
```css
@supports (display: grid) and (gap: 1rem) { .layout { display: grid; } }
@supports not (aspect-ratio: 1) { .thumb { padding-top: 100%; } }
@supports selector(:has(> img)) { .card:has(> img) { grid-template-rows: auto 1fr; } }
@supports font-tech(color-COLRv1) { .emoji { font-family: "Color Emoji COLRv1"; } }
@supports (anchor-name: --a) { /* anchor positioning layout */ }
```
JS: `CSS.supports("container-type: inline-size")`, `CSS.supports("selector(:popover-open)")`.

## 3. The selector list trap
One unknown selector invalidates the whole rule:
```css
input:focus-visible, input:-moz-focusring { outline: 2px solid; }   /* whole rule dropped where either is unknown */
```
Split into separate rules, or wrap in forgiving `:is()`/`:where()` (unknown entries inside are ignored).

## 4. The var() trap
A `var()` with a fallback is not feature detection: if the property value is invalid after substitution, the declaration becomes "invalid at computed-value time" and resets to `inherit`/`initial`, it does **not** fall back to an earlier declaration. Use `@supports` for new syntax inside custom properties.

## 5. Choosing what needs a fallback
Use Baseline status (Widely available = safe; Newly available = check your browserslist) and `@supports` only for features where the unsupported experience is broken, not merely plainer.

## Verify
- [ ] Test in the oldest browser in your support matrix with the enhancement disabled.

## Checked

Checked 2026-10-26 against current documentation. MDN `@supports` (`selector()`, `font-tech()`, `not`, mixing `and`/`or` needs parentheses), `:is()` forgiving selector parsing, `var()` fallback rules and the error-handling guide (invalid at computed-value time resets to inherited or initial value, not an earlier declaration).

Method: documentation only; no commands were run.
