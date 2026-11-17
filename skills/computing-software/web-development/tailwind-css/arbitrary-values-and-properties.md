---
id: computing-software.web-development.tailwind-css.arbitrary-values-and-properties
name: arbitrary-values-and-properties
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, arbitrary-values, arbitrary-properties, arbitrary-variants, css-variables, type-hints, web-development]
level: practitioner
status: verified
description: "Using Tailwind arbitrary values, CSS-variable shorthand, type hints, arbitrary properties and variants, and knowing when to promote them to theme tokens."
sources:
  - https://tailwindcss.com/docs/adding-custom-styles#using-arbitrary-values
  - https://tailwindcss.com/docs/detecting-classes-in-source-files#dynamic-class-names
  - https://tailwindcss.com/docs/hover-focus-and-other-states#using-arbitrary-variants
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arbitrary values, properties and variants

**Goal:** handle one-off values without leaving utility-first, while keeping the design system the default.

## 1. Arbitrary values
```html
<div class="top-[117px] grid-cols-[200px_minmax(0,1fr)] bg-[#bada55] w-[calc(100%-2rem)]">
```
- Spaces become underscores: `grid-cols-[1fr_auto]`. A literal underscore: `\_`.
- `calc()` needs no spaces in source; Tailwind adds them for operators.
- `var()` works inside brackets: `max-h-[calc(100dvh-var(--header))]`. `theme()` takes a theme variable name: `h-[theme(--spacing-header)]` resolved to `56px` for `--spacing-header: 56px` (run on 4.3.3), but `theme(--spacing-4)` generates nothing because v4 has one `--spacing` variable, not a per-step scale; use `theme(--spacing)` times a number or `calc(var(--spacing)*4)`. Underscore: `content-['a_b']` emits `'a b'`, `content-['a\_b']` emits `'a_b'` (run).

## 2. CSS variables shorthand
v4: `bg-(--brand-color)` = `bg-[var(--brand-color)]`. v3 used `bg-[--brand-color]`.
Set variables per element for runtime values (from JS or the CMS) instead of generating class names:
```jsx
<div style={{ "--progress": `${pct}%` }} className="w-(--progress) bg-green-600" />
```

## 3. Type hints when ambiguous
`text-[22px]` is font-size, `text-[#333]` is colour - inferred. With a variable Tailwind can't tell:
```html
<p class="text-(length:--title-size) text-(color:--title-color)">
```
Hints: `length`, `color`, `number`, `percentage`, `url`, `image`, `family-name`, etc.

## 4. Arbitrary properties
For CSS Tailwind has no utility for:
```html
<div class="[mask-type:luminance] hover:[mask-type:alpha] [--scroll-offset:56px]">
```

## 5. Arbitrary variants
```html
<li class="[&:nth-child(3)]:underline [&>svg]:size-4 [@supports(display:grid)]:grid [&_p]:mt-2">
```
`&` is the element; `_` is a descendant space.

## 6. Never build class names dynamically
Tailwind scans source text; `bg-${color}-500` is never generated. Map complete strings:
```js
const tone = { danger: "bg-red-500", ok: "bg-green-500" };
```

## 7. When to promote to a token
The same arbitrary value appearing three times is a design token. Add it to `@theme` (`--spacing-header: 56px;` → `h-header`) so it is named, themable and consistent.

## Verify
- [ ] `grep -rEo "\w+-\[[^]]+\]" src | sort | uniq -c | sort -rn | head` - repeated values reviewed for promotion.
- [ ] No template-literal class fragments (`grep -rn '\${' src | grep class`).
- [ ] Compiled CSS contains each arbitrary utility used.
