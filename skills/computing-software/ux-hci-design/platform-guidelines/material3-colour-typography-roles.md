---
id: computing-software.ux-hci-design.platform-guidelines.material3-colour-typography-roles
name: material3-colour-typography-roles
category: computing-software
field: ux-hci-design
product: platform-guidelines
tags: [material3-colour-roles, material3-type-scale]
level: practitioner
status: draft
description: "Use M3 colour roles for foreground and background pairs and the type scale (display, headline, title, body, label)."
sources:
  - https://m3.material.io/styles/color/roles
  - https://m3.material.io/styles/typography/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# M3 styles
- Roles: primary / on-primary, primary-container / on-primary-container, secondary, tertiary, error, surface, surface-variant, outline. Always pair "on-" roles with their container.
- Dynamic colour on Android 12+ derives a scheme from the wallpaper.
- Type scale: display, headline, title, body, label; each large/medium/small.
- Use roles in code (Compose `MaterialTheme.colorScheme`, `MaterialTheme.typography`) rather than hard-coded colours.

## Verify
- [ ] No hard-coded colours in components; both light and dark schemes render correctly.
