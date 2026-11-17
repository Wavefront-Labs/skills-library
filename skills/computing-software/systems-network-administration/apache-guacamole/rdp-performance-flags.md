---
id: computing-software.systems-network-administration.apache-guacamole.rdp-performance-flags
name: rdp-performance-flags
category: computing-software
field: systems-network-administration
product: apache-guacamole
tags: [systems-network-administration, apache-guacamole, rdp, performance-flags, enable-wallpaper, enable-theming, font-smoothing, desktop-composition, bitmap-caching, glyph-caching, offscreen-caching]
level: practitioner
status: draft
description: "Tune RDP visual features and caching in Guacamole: enable-wallpaper, theming, font smoothing, full-window-drag, desktop composition, menu animations, and the disable-*-caching flags."
sources:
  - https://guacamole.apache.org/doc/gug/configuring-guacamole.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# RDP performance flags

The `enable-*` visual features are off by default (best for low bandwidth). Set `true` to turn each on:
- `enable-wallpaper`: desktop wallpaper
- `enable-theming`: window and control theming
- `enable-font-smoothing`: smooth text edges (default is rough/jagged)
- `enable-full-window-drag`: show window contents while dragging
- `enable-desktop-composition`: transparency and shadows (Aero)
- `enable-menu-animations`: menu open/close animation

Caching switches, normally left alone:
- `disable-bitmap-caching=true`: turn off the RDP bitmap cache (work around known server bugs)
- `disable-offscreen-caching=true`: turn off off-screen region caching
- `disable-glyph-caching`: glyph caching is disabled regardless of this value (GUACAMOLE-1191)
- `disable-gfx=true`: drop back from the GFX pipeline (1.6.0)

Recipe:
1. LAN/fast: enable font smoothing and theming, leave the rest.
2. WAN: leave all flags off, lower `color-depth` (apache-guacamole.rdp-display-settings).
3. If artefacts or corruption appear, set the `disable-*-caching` flags one at a time.

Verify: compare perceived latency and bandwidth before and after changing one flag.
