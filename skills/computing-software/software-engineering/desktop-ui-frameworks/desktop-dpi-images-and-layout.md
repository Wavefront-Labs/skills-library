---
id: computing-software.software-engineering.desktop-ui-frameworks.desktop-dpi-images-and-layout
name: desktop-dpi-images-and-layout
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [desktop-dpi-images-and-layout, desktop-dpi-scaling, dpi, windows, cross-platform, desktop-ui-frameworks]
level: practitioner
status: draft
description: "Provide multi-scale assets and avoid pixel-based layout."
sources:
  - https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# DPI-independent assets and layout

**Goal:** consistent sizing.

```text
Use vector (SVG/XAML geometry) icons; or ship @1x @1.5x @2x @3x bitmaps
WPF: device-independent units (1/96 inch); BitmapScalingMode.HighQuality for scaled bitmaps
Qt: QIcon with multiple sizes; qt high-DPI scaling is on by default in Qt 6; QT_SCALE_FACTOR_ROUNDING_POLICY=PassThrough for fractional scales
Electron: window.devicePixelRatio, use CSS rem/vw, 'image-set()' for raster assets
```

**Gotcha:** Rounding fractional scales (125%, 150%) to integers makes UI too big or small; allow fractional scaling.

## Verify
- Screenshots at 125% and 175% look consistent.
