---
id: computing-software.ux-hci-design.design-systems.css-variables-theming-dark-mode
name: css-variables-theming-dark-mode
category: computing-software
field: ux-hci-design
product: design-systems
tags: [css-custom-properties-theming, dark-mode-theming, ds-theming]
level: practitioner
status: draft
description: "Implement light and dark themes using semantic CSS variables, prefers-color-scheme and a stored user override."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Theming
```css
:root { --bg:#fff; --fg:#111; color-scheme: light dark; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#0b0b0c; --fg:#eee; } }
:root[data-theme="dark"] { --bg:#0b0b0c; --fg:#eee; }
body { background:var(--bg); color:var(--fg); }
```
- Re-check contrast (4.5:1 / 3:1) in each theme; do not just invert.
- Elevate in dark mode with lighter surfaces rather than shadows.
- Desaturate large colour areas; test images and charts.
- Persist override; avoid flash by setting the attribute in `<head>` before paint.

## Verify
- [ ] Axe contrast checks pass in both themes.
