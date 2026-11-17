---
id: computing-software.web-development.tailwind-css.transition-animation-utilities-and-motion-safe
name: transition-animation-utilities-and-motion-safe
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind-animation, motion-safe, motion-reduce, tailwind-transitions, prefers-reduced-motion]
level: practitioner
status: docs-checked
description: "Animating with Tailwind: transition, duration and ease utilities, built-in animate-*, defining keyframes in @theme, starting: variant for entry, and motion-safe/motion-reduce."
sources:
  - https://tailwindcss.com/docs/transition-property
  - https://tailwindcss.com/docs/animation
  - https://tailwindcss.com/docs/transition-behavior
  - https://tailwindcss.com/docs/hover-focus-and-other-states
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailwind transition and animation utilities

## 1. Transitions
```html
<button class="bg-indigo-600 transition-colors duration-150 ease-out hover:bg-indigo-500
               motion-safe:transition-transform motion-safe:hover:-translate-y-0.5">
```
- Prefer the narrow utilities (`transition-colors`, `transition-opacity`, `transition-transform`) to avoid animating layout.
- `transition-discrete` enables transitions of discrete properties such as `display`; the default transition duration variable is 150ms.

## 2. Built-in and custom animations
`animate-spin`, `animate-ping`, `animate-pulse`, `animate-bounce`. Custom in v4:
```css
@theme {
  --animate-fade-up: fade-up .3s ease-out both;
  @keyframes fade-up { from { opacity: 0; translate: 0 .5rem; } }
}
```
Then `class="animate-fade-up"`. Define `@keyframes` inside `@theme` so they are included in the generated CSS.

## 3. Entry animations without JS (v4)
```html
<div popover class="opacity-100 transition-discrete transition-opacity starting:open:opacity-0">...</div>
```
Tailwind's `starting` variant is built on `@starting-style`, so newly displayed elements transition from the starting values.

## 4. Reduced motion
```html
<div class="motion-safe:animate-fade-up motion-reduce:animate-none"></div>
<svg class="animate-spin motion-reduce:animate-[spin_1.5s_linear_infinite]"></svg>
```
- `motion-safe:` = `@media (prefers-reduced-motion: no-preference)`; `motion-reduce:` = `reduce`.
- Prefer opting in with `motion-safe:` for decorative movement.
- Reduced motion means less movement, not no feedback: swap slides/zooms for fades.

## 5. Gotchas
- Arbitrary `animate-[<value>]` values reference an animation; declare keyframes in `@theme`.

## Checked

2026-11-01. Confirmed in Tailwind docs source: `animate-spin/ping/pulse/bounce`, `--animate-*` with `@keyframes` in `@theme`, `motion-safe`/`motion-reduce`, `animate-[<value>]`, `transition-discrete`, 150ms default duration variable, `@starting-style` section in states docs. Removed: v3 config note, transition property list, easing token names, spinner advice, same-frame gotcha.

Method: documentation only; no commands were run.

## Verify
- [ ] With "Reduce motion" enabled in the OS, decorative animation stops; transitions target only needed properties; entry animations play on first display.
