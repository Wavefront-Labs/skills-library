---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-dark-mode-ui
name: designing-dark-mode-ui
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [dark-mode-ui, dark-mode, dark-theme, dark-ui, surface-elevation, ui-color, theming]
level: practitioner
status: draft
description: "Design dark mode UI properly: dark grey surfaces not pure black, elevation by lighter surfaces, desaturated accents, contrast checks, and separate image and shadow handling."
sources:
  - "Material Design 3 - Dark theme (m3.material.io/styles/color/dark-theme)"
  - "Apple Human Interface Guidelines - Dark Mode (developer.apple.com/design/human-interface-guidelines/dark-mode)"
  - "WCAG 2.2 SC 1.4.3 Contrast (Minimum) (w3.org/TR/WCAG22)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dark mode UI

**Goal:** a dark theme that is comfortable, legible and consistent, not an inverted light theme.

## Principles
- **Surfaces:** use very dark greys (about #121212 to #1E1E1E) instead of pure black to reduce halation and allow elevation; true black (OLED) is a separate optional "black" mode.
- **Elevation:** lighter surface = higher elevation (overlay white at 5-16 percent), since shadows are invisible on dark.
- **Text:** off-white (about 87 percent opacity for primary, 60 for secondary, 38 for disabled in Material); pure white on black is harsh. Keep **4.5:1** for body, **3:1** for large text and UI.
- **Colour:** desaturate and lighten accents (shift toward tone 80 of a tonal ramp); saturated colours vibrate on dark surfaces.
- **Semantic colours** need dark-theme versions (`creative-arts.design-for-form-and-experience.interaction-design.designing-status-and-semantic-colours`).
- **Images and illustration:** avoid pure white backgrounds in images; supply dark variants or reduce brightness; vector icons should use currentColor; logos need a dark version.
- **Borders and dividers** at low-contrast white (8-12 percent); do not rely on borders alone.

## Implementing
- Design with **tokens**: semantic roles (surface, on-surface, primary) mapped per theme via variable modes (Figma) and CSS custom properties; respect `prefers-color-scheme` and offer a manual toggle that persists.
- `color-scheme: light dark;` so native controls match; set `<meta name="theme-color">` per scheme.
- Avoid flash on load by setting the theme before first paint.

## Verify
- [ ] Surfaces use elevation tint rather than shadows.
- [ ] All text and UI pairs pass contrast in dark.
- [ ] Theme follows system preference with a persisted override; images and logos handled.
