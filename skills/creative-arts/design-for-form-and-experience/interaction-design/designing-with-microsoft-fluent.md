---
id: creative-arts.design-for-form-and-experience.interaction-design.designing-with-microsoft-fluent
name: designing-with-microsoft-fluent
category: creative-arts
field: design-for-form-and-experience
product: interaction-design
tags: [fluent-design, fluent-2, microsoft-fluent, platform-guidelines, windows-design, fluent-ui, design-tokens]
level: practitioner
status: draft
description: "Design with Microsoft's Fluent 2 system: design tokens for colour, type, spacing and shape, Windows and web components, materials like Mica and Acrylic, and accessibility."
sources:
  - "Fluent 2 Design System (fluent2.microsoft.design)"
  - "Microsoft Learn - Windows app design: Fluent Design in Windows apps (learn.microsoft.com/windows/apps/design)"
  - "Fluent UI React v9 (react.fluentui.dev)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing with Microsoft Fluent 2

**Goal:** build experiences that fit Microsoft 365, Windows and Edge, using Fluent 2 tokens and components.

## Foundations
- **Tokens:** global (ramps) and alias tokens (neutral foreground1-3, background1-6, brand background, stroke), theme-able; light, dark and high-contrast themes; brand ramp generated from a brand colour (16 shades).
- **Typography:** Segoe UI Variable on Windows (Segoe UI / system on web); type ramp: Caption, Body 1, Subtitle, Title 3 down to Large Title and Display.
- **Spacing:** 4-pixel base unit scale (2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40...). **Corner radius:** 2, 4, 8, 12 px by component size. **Strokes:** 1 px default, thicker focus rings (2 px, with an inner and outer stroke).
- **Elevation:** shadow ramp (2, 4, 8, 16, 28, 64) with ambient and key shadows.
- **Materials:** Mica (opaque, wallpaper-tinted) for app backgrounds on Windows 11; Acrylic (translucent blur) for transient surfaces.
- **Iconography:** Fluent System Icons in regular and filled variants at 12-48 px.

## Layout and components
Responsive breakpoints (small, medium, large); command bars, navigation view (left pane), tabs, dialogs, cards, data grids. Use **Fluent UI React v9** (`FluentProvider` with `webLightTheme` / `webDarkTheme`) or WinUI 3 / Windows App SDK controls for native apps. Windows controls adopt system accent colour and rounded corners.

## Accessibility and input
High-contrast themes must work; keyboard navigation with visible focus; target sizes 32 px or larger on desktop and 40+ touch; Narrator support; support pen, touch and mouse.

## Process
1. Pick platform (web, Windows, iOS, Android) and the matching Fluent kit in Figma.
2. Theme with brand ramp; use alias tokens rather than raw hex values.
3. Test in light, dark and Windows high-contrast modes.

## Verify
- [ ] Tokens used for colour, spacing, radius and type; themes switch cleanly.
- [ ] High-contrast and keyboard focus verified.
