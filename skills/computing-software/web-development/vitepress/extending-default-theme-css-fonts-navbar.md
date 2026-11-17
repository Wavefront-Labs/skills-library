---
id: computing-software.web-development.vitepress.extending-default-theme-css-fonts-navbar
name: extending-default-theme-css-fonts-navbar
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, extend-default-theme, custom-css, vp-c-brand, css-variables, theme-without-fonts, inter-font, navbar-variables, backdrop-filter]
level: practitioner
status: docs-checked
description: "Customize the default theme with root CSS variables, swap the Inter font via theme-without-fonts, and restyle the navbar surface."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/extending-default-theme.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Entry file that keeps the default theme and adds CSS:

```js
// .vitepress/theme/index.js
import DefaultTheme from 'vitepress/theme'
import './custom.css'
export default DefaultTheme
```

```css
:root {
  --vp-c-brand-1: #646cff;
  --vp-c-brand-2: #747bff;
}
```

All variables are in the theme's `vars.css` in the VitePress repo.

**Fonts.** Inter ships and is preloaded by default. To avoid it, import from `vitepress/theme-without-fonts` and set `--vp-font-family-base` and `--vp-font-family-mono`. If you use optional components like the Team Page ones, import those from `theme-without-fonts` too. Local `@font-face` files become hashed assets under `dist/assets`; preload with `transformHead`:

```js
transformHead({ assets }) {
  const f = assets.find(file => /font-name\.[\w-]+\.woff2/.test(file))
  if (f) return [['link', { rel: 'preload', href: f, as: 'font', type: 'font/woff2', crossorigin: '' }]]
}
```

**Navbar variables** control one background surface: `--vp-nav-height`, `--vp-nav-bg-color`, `--vp-nav-home-bg-color` (transparent on unscrolled home; set it to `var(--vp-nav-bg-color)` to opt out), `--vp-nav-backdrop-filter`, `--vp-nav-divider-color`, `--vp-nav-screen-bg-color`. Frosted glass:

```css
:root {
  --vp-nav-bg-color: color-mix(in srgb, var(--vp-c-bg) 65%, transparent);
  --vp-nav-backdrop-filter: saturate(180%) blur(8px);
}
```

`--vp-local-nav-bg-color` follows the navbar colour. Warning: `backdrop-filter` costs scroll performance on large/high-DPI screens, check text contrast, and Safari 17 and earlier show the translucent colour without blur. When items do not fit, they collapse into the `...` menu (label via `extraMenuLabel`).

## Checked

2026-11-04. Confirmed against the VitePress extending-default-theme guide (Customizing CSS, Navbar variables and warning, Using Different Fonts, transformHead preload example) and the default-theme-config page (extraMenuLabel). Removed: the Verify step.

Method: documentation only; no commands were run.
