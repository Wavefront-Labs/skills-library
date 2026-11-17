---
id: creative-arts.comics-and-sequential-art.comic-colouring.colour-contrast-for-phone-screens
name: colour-contrast-for-phone-screens
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, digital-comic-colour, screen-contrast, mobile-colour, dark-mode, night-shift, readability, value-check]
level: practitioner
status: draft
description: "Colour for phone reading: value contrast that survives small screens, night modes and low brightness, avoiding crushed darks and neon fatigue, and testing on real devices."
sources:
  - https://webtoons-static.pstatic.net/creator101/en/pdf/Creators-Resource-Handbook-Updated.pdf
  - https://www.w3.org/TR/WCAG21/#contrast-minimum
  - https://en.wikipedia.org/wiki/Webtoon
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Colour contrast for phone screens

**Goal:** pages that read clearly on a phone at any brightness, including night-time
reading with warm filters on.

## Why it differs from print
- Small physical size: subtle value differences vanish.
- Readers lower brightness and enable night modes (warm colour shift), crushing dark
  and blue-heavy scenes.
- OLED screens show deep blacks but can band in dark gradients.

## Practices
1. **Value separation**: check the page in greyscale at phone size; figure and ground
   should differ clearly. Increase separation more than you would for print.
2. **Avoid crushed darks**: night scenes in mid-dark values with rim light, not near
   black everywhere. Keep detail above ~10-15% brightness.
3. **Saturation**: pure saturated neon backgrounds tire eyes in scroll formats; reserve
   them for accents.
4. **Text**: balloon text black on white (or high-contrast equivalents). For coloured
   captions, aim for high contrast; WCAG's 4.5:1 text contrast guideline is a useful
   reference.
5. **Banding**: add slight noise/grain to large dark gradients before export.

## Testing
- View on at least one phone at low brightness and with night mode on.
- Check iOS and Android if possible (different panels and default colour handling).

## Verify
- [ ] Greyscale phone-size check passes.
- [ ] Dark scenes readable at low brightness with night mode.
- [ ] Text contrast high in all balloons/captions.
