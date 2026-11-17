---
id: computing-software.web-development.web-accessibility.three-flashes-and-seizure-safety
name: three-flashes-and-seizure-safety
category: computing-software
field: web-development
product: web-accessibility
tags: [enough-time, seizure-safety, three-flashes, wcag-2-3-1, photosensitive-epilepsy, flash-threshold, red-flash, peat-tool]
level: practitioner
status: verified
description: "Meeting WCAG 2.3.1 Three Flashes: what counts as a flash, general and red flash thresholds, testing video and animation with PEAT/Harding, and safe design limits."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
  - https://trace.umd.edu/peat/
  - https://www.w3.org/TR/WCAG22/#dfn-general-flash-and-red-flash-thresholds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Three flashes and seizure safety

**Goal:** nothing on the page can trigger photosensitive seizures.

## 1. The rule (2.3.1, A)
Content doesn't flash more than **three times in any one-second period**, or the flashing is below the general and red flash thresholds. Like 2.2.2, it's non-interference: a violation anywhere on the page fails it, and it applies even to content users didn't choose to play.

## 2. Thresholds (simplified)
- **General flash** (WCAG definition): a pair of opposing changes in relative luminance of 10% or more of the maximum relative luminance (1.0), where the darker image is below 0.80.
- **Passes if** there are no more than three general flashes and no more than three red flashes in any one second, or the combined concurrent flash area is no more than 0.006 steradians within any 10 degree visual field (25% of it); the Understanding page translates this to a 341 x 256 CSS px block (87,296 px), based on a 1024x768 reference screen.
- **Red flash**: any pair of opposing transitions involving saturated red, defined as R/(R+G+B) of at least 0.8 with a chromaticity difference above 0.2 (CIE 1976 UCS) between states; counted separately.
2.3.2 (AAA) removes the area allowance: no more than three flashes per second at all.

## 3. Risky content
Strobe effects in video/ads, rapid alternating dark/light backgrounds, glitch effects, fast-blinking alerts, game hit effects, scroll-driven colour flicker, high-contrast stripes or checkerboards moving quickly.

## 4. Testing
- Video and animation: Trace Center **PEAT** (free Windows-era download; its terms prohibit using it to assess TV broadcast, film, home-entertainment or gaming material) or Harding FPA from Cambridge Research Systems (for broadcast, film and games) analyse recordings for flash and red-flash failures. Record screen captures of animated UI at 60 fps and run them through.
- Design rule of thumb: never alternate large areas of strongly contrasting colours faster than 3 Hz; keep blinking indicators ≤ 1-2 Hz and small.

## 5. Mitigations
- Remove or slow the effect; reduce contrast/area of the flashing region.
- Give warnings before user-initiated media known to contain flashing (doesn't satisfy 2.3.1 for autoplay content).
- Honour `prefers-reduced-motion` to switch off effects (helpful, not a substitute for meeting the threshold).

## Verify
- [ ] PEAT/Harding pass for all video and animated hero content.
- [ ] No blinking UI faster than 3 per second.
- [ ] Ads/third-party creatives covered by contract and spot-checks.
