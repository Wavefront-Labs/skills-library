---
id: computing-software.web-development.tailwind-css.production-build-purging-and-performance
name: production-build-purging-and-performance
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, jit, content-globs, purge, dynamic-classnames, build-performance, css-bundle, web-development]
level: advanced
status: verified
description: "Tailwind's JIT content scanning: why dynamically-constructed class strings silently vanish from the production build, and how to avoid it."
sources:
  - https://tailwindcss.com/docs/content-configuration
  - https://tailwindcss.com/docs/optimizing-for-production
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tailwind production builds — content scanning and the dynamic class trap

**Goal:** understand that Tailwind's small production CSS bundle comes from
*not generating* classes it can't find as complete strings in your source — so
the #1 production bug is a class that exists in the DOM but not in the CSS.

## 1. How the JIT engine actually finds classes
Tailwind doesn't know your app's logic — it scans the files matched by
`content` (the config glob) as plain text, looking for substrings that look
like utility classes, and generates CSS only for what it finds. There's no
JS evaluation, no tracing of variables — it is a text scan.
```js
// tailwind.config.js
content: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
```
A file not matched by this glob (a `.mdx` file, a shared component in a
different package not included) silently loses its classes with no error —
the build succeeds, the class just never makes it into the CSS, and the
element renders unstyled. Check `content` globs cover every file type and
directory that contains class strings, including a monorepo's shared UI
package if styles are generated per-app.

## 2. The dynamic class name trap — this is the most common real bug
```jsx
// BREAKS: Tailwind never sees the complete string "text-red-500" or "text-green-500"
<div className={`text-${color}-500`}>
// WORKS: both complete class strings exist literally in the source for the scanner to find
<div className={color === 'error' ? 'text-red-500' : 'text-green-500'}>
```
Because the scanner works on literal substrings, `text-${color}-500` is never a
match for any generated class — it's invisible to the content scan regardless
of what `color` evaluates to at runtime. The fix is always to write out every
complete class string literally, even inside a ternary/object map:
```jsx
const colorMap = { error: 'text-red-500', success: 'text-green-500' };
<div className={colorMap[status]}>   // both full strings appear literally in this file
```
This also applies to classes built from a CMS/database-driven value (an admin
lets a user pick a "theme color" stored as a string) — those classes can never
be purged-in correctly since they don't exist in source at build time at all;
either whitelist the exact set of possible classes via a `safelist` entry in
config, or generate the color via a CSS variable instead of a dynamic utility.

## 3. `safelist` — the escape hatch, used sparingly
```js
safelist: ['bg-red-500', 'bg-green-500', { pattern: /bg-(red|green|blue)-(100|500)/ }],
```
Run on 3.4.19: that one pattern emitted 44 rules for `bg-blue-100` alone (the plain class plus its `/0` to `/100` opacity forms), and the v3 docs say a pattern only matches base utility names, so add `variants: ['hover']` for variants. This page describes v3 `content`/`safelist`; v4 detects sources automatically and uses `@source` and `@source inline()`, see dynamic-class-names-and-safelisting.
Forces specific classes (or a regex pattern) into the output regardless of
whether the scanner finds them in source — necessary for genuinely
runtime-determined classes (CMS content, a class name assembled from an API
response) but it defeats the purge benefit for everything it covers, so keep
the pattern as narrow as the real possible value set.

## 4. Build performance at scale
JIT scanning cost scales with the number and size of files matched by
`content` — an overly broad glob (`./**/*` catching `node_modules` because an
exclude was forgotten) slows every build significantly and can pull
third-party class-like strings into the scan. Scope globs as tightly as
possible to actual source directories.

## 5. Checking what actually shipped
`npx tailwindcss -i input.css -o output.css --minify` then search the output
for an expected class directly — if it's missing, the content glob or a
dynamic-string issue is the cause, not a syntax error in your HTML/JSX.
Browser DevTools showing an element with the right class attribute but no
matching CSS rule is the signature symptom.

## Verify
- [ ] `content` globs cover every file type/location (including shared/monorepo packages) that contains class strings.
- [ ] No class name is built via string interpolation (`` `text-${x}-500` ``) — every full class string appears literally in source.
- [ ] Any genuinely runtime-driven class value is covered by an explicit, narrow `safelist` pattern.
- [ ] The production CSS output was checked directly for an expected class when a style unexpectedly doesn't apply.
- [ ] `content` globs exclude `node_modules` and build output directories to keep scan time reasonable.
