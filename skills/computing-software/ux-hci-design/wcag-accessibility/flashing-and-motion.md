---
id: computing-software.ux-hci-design.wcag-accessibility.flashing-and-motion
name: flashing-and-motion
category: computing-software
field: ux-hci-design
product: wcag-accessibility
tags: [three-flashes]
level: practitioner
status: docs-checked
description: "Keep content to no more than three flashes per second or below the flash thresholds (SC 2.3.1) and test with analysis tools."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# 2.3.1 Three Flashes or Below Threshold (A)
- Web pages must not contain anything that flashes more than three times in any one second period, or the flash must be below the general flash and red flash thresholds.
- A general flash is a pair of opposing changes in relative luminance of 10% or more of the maximum relative luminance where the darker image's relative luminance is below 0.80. A red flash is a pair of opposing transitions involving saturated red.
- Content that flashes three or fewer times in any one second passes without a tool. Otherwise use an analysis tool; the page names the Harding FPA and the Trace Center Photosensitive Epilepsy Analysis Tool (PEAT), and technique G15 (a tool to check the general and red flash thresholds).
- Turning the flash off is not an acceptable solution, since a seizure could occur faster than most users could switch it off.
- Example from the page: a movie scene edited so lightning only flashes three times in any one second.

## Verify
- [ ] Count flashes per second, or run the content through a flash analysis tool.

## Checked

2026-11-09. Confirmed on the Understanding SC 2.3.1 page: the criterion text and level, the general flash and red flash definitions, the pass-without-tool rule, the named tools, G15, and the note that turning off the flash is not an option. Removed: the SC 2.3.3 bullet, the prefers-reduced-motion CSS, the vestibular remark and its verify step, none of which this page covers.

Method: documentation only; no commands were run.
