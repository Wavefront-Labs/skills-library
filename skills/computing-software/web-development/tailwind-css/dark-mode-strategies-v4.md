---
id: computing-software.web-development.tailwind-css.dark-mode-strategies-v4
name: dark-mode-strategies-v4
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-dark-mode, dark-mode, custom-variant, prefers-color-scheme, color-scheme, theming, web-development]
level: practitioner
status: verified
description: "Implementing dark mode in Tailwind v4: media default, class or data-attribute variants via @custom-variant, a no-flash three-way toggle and token-based theming."
sources:
  - https://tailwindcss.com/docs/dark-mode
  - https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dark mode strategies in Tailwind v4

**Goal:** dark mode that follows the OS by default, allows a user override, and never flashes the wrong theme.

## 1. Pick the strategy
| Strategy | Config | Use when |
|---|---|---|
| Media (default) | nothing | no in-app toggle needed |
| Class | `@custom-variant dark (&:where(.dark, .dark *));` | toggle via `.dark` on `<html>` |
| Data attribute | `@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));` | multiple themes, matches design-system attributes |

v3 equivalent: `darkMode: 'media'`, `'selector'` or `['selector', '[data-theme="dark"]']` (`selector` replaced `class` in v3.4.1; `'class'` still compiled in 3.4.19). All of these, and the three v4 rows above, were compiled and the generated `dark:` selectors inspected.

## 2. No-flash three-way toggle (light / dark / system)
Inline in `<head>` before CSS paints, not in a framework mount hook:
```html
<script>
  const t = localStorage.theme;
  const dark = t === "dark" || (!t && matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.classList.toggle("dark", dark);
</script>
```
On user choice: set or `localStorage.removeItem("theme")` for system, then re-run the toggle. Listen to `matchMedia(...).addEventListener("change", ...)` when on system. With a strict CSP, give the script a nonce or hash.
SSR frameworks: next-themes avoids the flash with an injected inline script plus `localStorage` (not a cookie) and needs `suppressHydrationWarning` on `<html>`; delay rendering any theme-toggle UI until mounted. Rendering the class server-side from a cookie is a separate approach you would build yourself.

## 3. Tell the browser too
```css
:root { color-scheme: light; }
:root.dark { color-scheme: dark; }
```
This themes scrollbars, form controls and the default canvas. Without it you get white scrollbars on dark pages.

## 4. Prefer tokens over `dark:` everywhere
```css
@theme { --color-surface: #fff; --color-ink: #111827; }
@layer base {
  .dark { --color-surface: #0b1020; --color-ink: #e5e7eb; }
}
```
Markup uses `bg-surface text-ink` once; dark values live in one place. Keep `dark:` for genuine one-offs (an image swap, a shadow that should disappear).

## 5. Details
- Images: `<picture><source srcset="logo-dark.svg" media="(prefers-color-scheme: dark)">` only follows the OS; with a class toggle use `dark:hidden` / `hidden dark:block` pairs.
- Elevation in dark mode: lighter surfaces, not darker shadows.
- Re-check contrast for every token pair in both themes (WCAG 4.5:1 body text).

## Verify
- [ ] Hard-reload with the dark preference: no light flash (throttle CPU 6x in DevTools to see it).
- [ ] System / light / dark all persist across reloads; "system" follows an OS change live.
- [ ] Native controls and scrollbars are dark in dark mode.
