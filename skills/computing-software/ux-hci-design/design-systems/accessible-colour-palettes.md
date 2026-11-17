---
id: computing-software.ux-hci-design.design-systems.accessible-colour-palettes
name: accessible-colour-palettes
category: computing-software
field: ux-hci-design
product: design-systems
tags: [accessible-colour-palette, tonal-palette]
level: advanced
status: draft
description: "Build tonal palettes where defined step pairs meet contrast thresholds, using perceptual colour spaces."
sources:
  - https://m3.material.io/styles/color/system/overview
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accessible palettes
- Build 10-12 step tonal scales in a perceptual space (HCT in Material 3, OKLCH elsewhere) so that lightness steps relate predictably to contrast.
- Pre-validate pairings: text-on-surface roles at 4.5:1; UI boundaries 3:1.
- Material 3 colour roles (primary, on-primary, primary-container, surface, etc.) pair foreground and background roles so contrast is built in.
- Colour-blind check: do not rely on red vs green alone.

## Verify
- [ ] Automated contrast test over all declared foreground and background token pairs.
