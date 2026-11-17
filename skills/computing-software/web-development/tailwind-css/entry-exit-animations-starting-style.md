---
id: computing-software.web-development.tailwind-css.entry-exit-animations-starting-style
name: entry-exit-animations-starting-style
category: computing-software
field: web-development
product: tailwind-css
tags: [css-animations, css-transitions, starting-style, allow-discrete, transition-behavior, display-none-transition, popover-animation, dialog-animation]
level: practitioner
status: verified
description: "Animating elements in from display:none and out again using @starting-style and transition-behavior allow-discrete, for dialogs, popovers and toasts."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style
  - https://developer.mozilla.org/en-US/docs/Web/CSS/transition-behavior
  - https://developer.chrome.com/blog/entry-exit-animations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Entry/exit animations with @starting-style

**Goal:** fade/slide elements in when they appear (from `display: none` or newly inserted) and out when they hide, with CSS transitions only.

## 1. The problem
Transitions don't run on first render (no "before" style) and `display` is discrete (can't be interpolated), so `display: none` -> `block` jumps instantly and hiding snaps away before the fade.

## 2. The pattern (popover / dialog)
```css
[popover], dialog {
  opacity: 0; transform: translateY(8px);
  transition: opacity .2s, transform .2s, overlay .2s allow-discrete, display .2s allow-discrete;
}
[popover]:popover-open, dialog[open] { opacity: 1; transform: none; }
@starting-style {
  [popover]:popover-open, dialog[open] { opacity: 0; transform: translateY(8px); }
}
dialog::backdrop { background: rgb(0 0 0 / 0); transition: background .2s, overlay .2s allow-discrete, display .2s allow-discrete; }
dialog[open]::backdrop { background: rgb(0 0 0 / .4); }
@starting-style { dialog[open]::backdrop { background: rgb(0 0 0 / 0); } }
```
- `@starting-style` provides the "from" values for the first style computation (entry).
- `transition-behavior: allow-discrete` (or `allow-discrete` in the shorthand) makes `display` and `overlay` flip at the **end** of the exit transition, so the element stays visible while fading out.
- `overlay` keeps top-layer elements (dialog, popover) in the top layer during the exit.
- `@starting-style` must come **after** the open-state rule (same specificity, order matters) or be nested inside it.

## 3. Newly inserted elements (toasts)
```css
.toast { transition: opacity .2s, translate .2s; }
@starting-style { .toast { opacity: 0; translate: 0 1rem; } }
```
Exit for removed elements still needs JS (animate, then remove) or a hidden state class with `allow-discrete`.

## 4. Support
Chromium 117+, Safari 17.5+ (for `@starting-style`/`allow-discrete`); Firefox supports `@starting-style` from 129 but not animating `overlay`. Without support, elements just appear/disappear - acceptable degradation.

## Verify
- [ ] Opening and closing a popover/dialog animates both ways; focus handling unaffected.
- [ ] Reduced-motion users get opacity only (or instant).
- [ ] No flash of the open state before the entry transition.
