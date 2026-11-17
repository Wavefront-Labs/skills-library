---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-with-material-design-3
name: designing-with-material-design-3
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [material-design, material-design-3, platform-guidelines, material-you, m3, dynamic-color, android-design]
level: practitioner
status: draft
description: "Design Android and web UI with Material Design 3: dynamic colour roles, type scale tokens, shape and elevation, adaptive layouts, components and the Material Theme Builder."
sources:
  - "Material Design 3 (m3.material.io) - Foundations, Styles, Components"
  - "Material Theme Builder (m3.material.io/theme-builder)"
  - "Android Developers - Material 3 in Compose and adaptive layouts (developer.android.com/develop/ui/compose/designsystems/material3)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing with Material Design 3

**Goal:** use M3 as a coherent system, adapting its tokens to your brand rather than copying defaults.

## Foundations
- **Colour roles:** primary, secondary, tertiary, error, neutral, neutral-variant; each with `on-` counterparts and container roles (primary-container, on-primary-container); surface tones (surface, surface-container-lowest to highest). Generate a tonal palette from a **source colour** in Material Theme Builder (13 tones per palette, tone 0-100); light and dark schemes derive from the same palette. **Dynamic colour** on Android 12+ extracts a scheme from the wallpaper.
- **Typography:** five roles (display, headline, title, body, label) x three sizes (large, medium, small) = 15 type tokens, with default Roboto but any font.
- **Shape:** corner-radius scale from none to extra-large to full (0, 4, 8, 12, 16, 28, 50 percent); components map to a shape token.
- **Elevation:** tonal surface colour plus optional shadow, six levels (0-5).
- **Motion:** easing tokens (emphasized, standard) and durations.
- **State layers:** hover (8%), focus (10%), pressed (10%), dragged (16%) opacity overlays.

## Layout
Window size classes: compact (under 600 dp), medium (600-839), expanded (840+); canonical layouts (list-detail, supporting pane, feed); navigation bar to rail to drawer as width grows; 4/8/12 columns.

## Components
Use the M3 component set (buttons: filled, tonal, outlined, text, elevated; FAB; chips; cards; top app bar; navigation bar; dialogs; snackbars; text fields) with state specs. In Figma use the Material 3 Design Kit; in code, Compose Material 3 or Material Web (`@material/web`).

## Process
1. Pick a source colour, generate the theme, export tokens.
2. Map tokens to components; override only where brand demands, preserving contrast (check 4.5:1 for text roles).
3. Test across window classes, dark theme, large font scale and dynamic colour.

## Verify
- [ ] Colour, type and shape come from tokens, not hard-coded values.
- [ ] Layouts adapt across compact, medium and expanded widths.
- [ ] Contrast and state layers verified in light and dark.
