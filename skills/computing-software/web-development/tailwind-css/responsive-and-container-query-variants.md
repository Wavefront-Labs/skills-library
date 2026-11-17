---
id: computing-software.web-development.tailwind-css.responsive-and-container-query-variants
name: responsive-and-container-query-variants
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-responsive, tailwind-container-queries, breakpoints, mobile-first, container-queries, web-development]
level: practitioner
status: verified
description: "Responsive Tailwind: mobile-first breakpoints, max-* ranges, custom breakpoints in @theme, and container-query variants including named containers."
sources:
  - https://tailwindcss.com/docs/responsive-design
  - https://tailwindcss.com/docs/responsive-design#container-queries
  - https://tailwindcss.com/docs/theme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responsive and container-query variants

**Goal:** layouts that adapt to the viewport for page structure and to the container for reusable components.

## 1. Mobile-first breakpoints (v4 defaults)
| Prefix | min-width |
|---|---|
| `sm` | 40rem (640px) |
| `md` | 48rem (768px) |
| `lg` | 64rem (1024px) |
| `xl` | 80rem (1280px) |
| `2xl` | 96rem (1536px) |

Unprefixed = all sizes. `sm:` means "640px **and up**", not "small screens". Style mobile first, then add larger overrides:
```html
<div class="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
```

## 2. Ranges and max-*
```html
<nav class="max-md:hidden">               <!-- below md only -->
<p class="md:max-xl:text-lg">            <!-- md up to (not incl.) xl -->
<div class="min-[900px]:flex max-[1100px]:gap-2">  <!-- one-off -->
```

## 3. Custom breakpoints
```css
@theme {
  --breakpoint-xs: 30rem;
  --breakpoint-3xl: 120rem;
  --breakpoint-2xl: initial; /* remove one */
}
```
Use rem so breakpoints track user font-size. Keep units consistent (mixing px and rem breaks sort order). v3: `theme.screens` in JS config.

## 4. Container queries (built into v4; v3 needs `@tailwindcss/container-queries`)
```html
<div class="@container">
  <article class="flex flex-col @md:flex-row @max-xs:text-sm">...</article>
</div>
```
- `@container` marks the query container (`container-type: inline-size`).
- `@sm`…`@7xl` are container sizes (`@md` = 28rem) - different from viewport `md`.
- Named: `@container/sidebar` then `@lg/sidebar:grid-cols-2` when nested containers exist.
- Arbitrary: `@min-[400px]:`.
- Container query units: `w-[50cqw]`.

## 5. Which to use
Page skeleton (sidebar shows/hides, nav collapses) → viewport breakpoints. Cards, media objects, widgets that appear in sidebars and main columns → container queries.

## Gotchas
- A container can't size itself from its own content: `inline-size` containment means a shrink-to-fit parent collapses. Give it a width (block-level or `w-full`).
- `hidden md:block` hides from assistive tech too; fine for duplicate nav, wrong for content.

## Verify
- [ ] Test at 320px, 768px, 1024px, 1440px and with 200% browser zoom.
- [ ] Reusable components render correctly in the narrowest slot they appear in.
- [ ] No `sm:` used where "mobile only" was intended (should be unprefixed + `sm:` override, or `max-sm:`).
