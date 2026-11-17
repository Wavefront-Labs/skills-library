---
id: computing-software.web-development.tailwind-css.color-mix-and-relative-colors
name: color-mix-and-relative-colors
category: computing-software
field: web-development
product: tailwind-css
tags: [css-color, color-mix, relative-color, color-functions, hover-states, alpha-variants, design-tokens, relative-color-syntax]
level: practitioner
status: verified
description: "Deriving colours in CSS with color-mix() and relative colour syntax: hover/active shades, alpha variants from tokens, tints in OKLCH, and fallbacks."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/color-mix
  - https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_colors/Relative_colors
  - https://developer.chrome.com/blog/css-relative-color-syntax
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# color-mix() and relative colours

**Goal:** derive hover states, borders, translucent variants and tints from a few base tokens instead of hard-coding every shade.

## 1. color-mix()
```css
:root { --brand: oklch(55% 0.2 260); --surface: white; }
.btn { background: var(--brand); }
.btn:hover { background: color-mix(in oklch, var(--brand), black 12%); }
.btn:active { background: color-mix(in oklch, var(--brand), black 20%); }
.badge { background: color-mix(in srgb, var(--brand) 15%, transparent); }       /* translucent tint */
.card { border-color: color-mix(in oklch, var(--brand) 25%, var(--surface)); }
```
- Interpolation space matters: `in oklch`/`in oklab` give perceptually smooth mixes; `in srgb` can go muddy/grey mid-way between complementary colours.
- Mixing with `transparent` creates alpha variants from a token whose value you don't control (Tailwind v4 uses this for `bg-blue-500/50`).

## 2. Relative colour syntax
```css
.btn:hover { background: oklch(from var(--brand) calc(l - 0.08) c h); }      /* darker by fixed lightness */
.ghost { background: rgb(from var(--brand) r g b / 10%); }                    /* same colour, 10% alpha */
.complement { color: oklch(from var(--brand) l c calc(h + 180)); }
```
Channel keywords (`l c h`, `r g b`, `alpha`) refer to the origin colour converted into the target space. In OKLCH relative syntax, `l` is a number 0-1 in current spec/implementations - don't mix `%` and numbers inconsistently.

## 3. Support and fallback
`color-mix()`: all current engines. Relative colour syntax: all current engines more recently (Firefox 128+, Safari 18+). Provide a static fallback before the derived declaration for older browsers:
```css
.btn:hover { background: #1e40af; background: oklch(from var(--brand) calc(l - 0.08) c h); }
```

## 4. Theming
Derive from tokens per theme so dark mode only redefines base tokens; derived states follow automatically. Check contrast of derived colours - mixing can push text/background pairs below 4.5:1.

## Verify
- [ ] Hover/active/disabled states derive from one token; changing the token updates all.
- [ ] Derived pairs meet contrast in light and dark themes.
- [ ] Fallback colours render in the oldest supported browser.
