---
id: computing-software.web-development.tailwind-css.dynamic-class-names-and-safelisting
name: dynamic-class-names-and-safelisting
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind-safelist, dynamic-class-names, source-inline, class-detection, tailwind-v4, tailwind]
level: practitioner
status: verified
description: "Why Tailwind misses dynamically built class names, mapping to complete class strings, CSS-variable arbitrary values, @source inline safelisting in v4 and scanning node_modules."
sources:
  - https://tailwindcss.com/docs/detecting-classes-in-source-files
  - https://tailwindcss.com/docs/detecting-classes-in-source-files#safelisting-specific-utilities
  - https://v3.tailwindcss.com/docs/content-configuration#safelisting-classes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic class names and safelisting

Tailwind scans source files as plain text for complete class tokens. It does not run your code, so it never sees `bg-${color}-500`.

## 1. Map to complete strings
```tsx
const tone = {
  info:    "bg-blue-50 text-blue-900 border-blue-200",
  warning: "bg-amber-50 text-amber-900 border-amber-200",
  danger:  "bg-red-50 text-red-900 border-red-200",
} as const;
<div className={`rounded border p-3 ${tone[variant]}`} />
```
The full strings exist in source, so they are generated. Libraries like `cva` follow the same principle.

## 2. Truly dynamic values (CMS colours, user themes)
Use a CSS variable and an arbitrary value that references it:
```tsx
<button style={{ "--brand": user.color } as React.CSSProperties} className="bg-(--brand) hover:opacity-90" />
```
v4 syntax `bg-(--brand)`; v3 `bg-[var(--brand)]`. One class covers infinite values.

## 3. Safelisting
v4.1+:
```css
@import "tailwindcss";
@source inline("bg-red-500 text-white");
@source inline("{hover:,}bg-{red,green,blue}-{100,500,900}");   /* brace expansion */
@source not inline("container");                                 /* never generate */
```
v3: `safelist: ["bg-red-500", { pattern: /bg-(red|green|blue)-(100|500)/, variants: ["hover"] }]` in `tailwind.config.js` (run on 3.4.19; the v3 docs say patterns match base utility names only and variants come from the `variants` option).
Safelist sparingly: a v3 pattern also pulled in the opacity-modifier forms (the example above generated 44 `bg-blue-100` rules, from `bg-blue-100` to `bg-blue-100/100`), so patterns can generate thousands of rules. `@source inline()` arrived in Tailwind v4.1.0 (changelog); the brace expansion above, `{hover:,}bg-{red,green}-{100,500}`, compiled to the plain and `hover:` forms of all four colours (run on 4.3.3).

## 4. Files Tailwind does not scan
v4 auto-detects sources but ignores `.gitignore`d paths and `node_modules`. Class names inside a UI package or templates outside the project root need:
```css
@source "../node_modules/@acme/ui/dist";
@source "../../packages/shared/src";
```
Classes stored in a database or CMS content need safelisting or the CSS-variable pattern.

## Verify
- [ ] Search the built CSS for a class used only via a variant map or CMS; it exists. No `bg-${...}` template literals remain (lint with a custom rule or grep).
