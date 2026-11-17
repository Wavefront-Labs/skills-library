---
id: creative-arts.graphic-design.brand-identity.responsive-logo-versions
name: responsive-logo-versions
category: creative-arts
field: graphic-design
product: brand-identity
tags: [graphic-design, brand-identity, logo-design, logo, responsive-logo, logo-scalability, favicon, app-icon, small-size-version, minimum-size, simplified-mark, social-avatar]
level: practitioner
status: draft
description: "Design a logo family that works at every size: full lockup, compact, symbol-only and favicon versions, minimum sizes, small-size simplifications, and app/social avatars."
sources:
  - https://developer.apple.com/design/human-interface-guidelines/app-icons
  - https://www.wiley.com/en-us/Designing+Brand+Identity%3A+A+Comprehensive+Guide+to+the+World+of+Brands+and+Branding%2C+6th+Edition-p-9781119775638
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Responsive logo versions

**Goal:** the brand stays recognisable from a billboard to a 16 px browser tab.

## The family (from largest to smallest)
1. **Primary lockup:** symbol + wordmark (+ tagline) - large formats, first impressions.
2. **Horizontal and stacked** lockups for different spaces (see lockups skill).
3. **Compact:** wordmark only or symbol + short name - headers, small print.
4. **Symbol / monogram only** - social avatars, app icons, merchandise, watermarks.
5. **Favicon / micro version:** simplified symbol for 16-32 px; fewer details, heavier strokes, maybe one letter.

## Simplify for small sizes
- Remove fine details, thin lines, small counters and taglines below a set size.
- Increase stroke weight and spacing slightly (optical sizing), open up counters.
- Test on real devices: browser tab (16x16 and 32x32), iOS/Android home screens, social profile circles
  (crops to a circle - keep the symbol inside ~80% of the square).

## Minimum sizes
Define for each version in print (mm) and screen (px), e.g. primary lockup >= 25 mm / 120 px wide, symbol >= 8 mm / 24 px.
Below that, switch to the next simpler version.

## Delivery
- Favicon set: `favicon.ico` (16/32/48), `apple-touch-icon.png` 180x180, SVG favicon for modern browsers, Android
  icons via web manifest (192 and 512 px), maskable icon with safe zone.
- App icons: follow platform templates (Apple: 1024x1024 master, no transparency; system applies corner masks).
- Social avatars: 400x400+ square, symbol centred within the circular crop.
See logo file delivery skill for the full package.

## Gotchas
- Shrinking the primary lockup instead of switching versions makes taglines and wordmarks illegible.
- Wordmarks with very light weights disappear in small UI contexts - provide a heavier small-size cut.

## Verify
- [ ] Each version defined with a minimum size; switch points documented.
- [ ] Favicon and avatars tested on real devices and circle crops.
