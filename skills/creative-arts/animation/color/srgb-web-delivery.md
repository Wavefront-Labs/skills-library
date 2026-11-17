---
id: creative-arts.animation.color.srgb-web-delivery
name: srgb-web-delivery
category: creative-arts
field: animation
product: color
tags: [srgb-delivery, display-standards, srgb, web-video, browser-colour, gamma-mismatch, icc-profile, youtube, social-video]
level: practitioner
status: draft
description: "Make web and social deliveries look as graded across browsers and phones: sRGB vs BT.1886 viewing, tagging choices, ICC for stills, testing on real devices."
sources:
  - https://www.w3.org/Graphics/Color/sRGB.html
  - https://www.itu.int/rec/R-REC-BT.1886
  - https://support.google.com/youtube/answer/1722171
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sRGB and web delivery

**Goal:** web viewers see the grade you approved. Browsers, phones and OS video pipelines decode
the same BT.709-tagged file differently; animation's flat midtones and saturated colours expose the
differences.

## What actually happens

- Most browsers decode BT.709 video and display it close to the sRGB/2.2 curve on the user's
  display, which reads lighter in the shadows than a gamma 2.4 grading monitor.
- macOS/iOS colour-manage video using the tags; Chrome/Windows often do less management.
- Untagged files get guesses: often BT.601 matrix for SD sizes (colour shift) and an unknown curve.

## Choose a show policy

| Audience | Grade on | Tag |
|---|---|---|
| TV/streaming first, web second | gamma 2.4, Rec.709 | `bt709` everywhere |
| Web/phone first (YouTube channel, social) | gamma 2.2 (or sRGB) in a normally lit room | `bt709` primaries/matrix; transfer `bt709` (most compatible) |

Whatever you choose: always tag primaries, matrix and range
(`creative-arts.animation.encode-delivery.colour-metadata-tags`), and never bake a "web gamma fix"
curve into one deliverable only.

## Stills and thumbnails

- Export thumbnails and posters as sRGB with an embedded sRGB ICC profile (or Display P3 profile if
  intentionally wide-gamut). Strip-profile pipelines make them look dull on wide-gamut phones.
- PNG frames grabbed from the grade must go through the output transform, not saved from the
  working space.

## Test matrix

Upload privately and check on: Chrome on Windows, Safari on macOS, iPhone, an Android phone, and a
TV app. Look at a dark shot, a skin/character colour shot, and a saturated FX shot.

## Gotchas

- Uploading H.264 already graded for 2.2 and then also tagging sRGB transfer can double the
  correction on Apple devices.
- Platform re-encodes keep tags if present; missing tags are not fixed by the platform.

## Verify

The same frame from the upload, captured on two browsers, is within a small visible difference of the
grading reference; dark scenes are not crushed or lifted grey on any test device.
