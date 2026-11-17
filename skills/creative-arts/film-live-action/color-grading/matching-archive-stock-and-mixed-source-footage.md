---
id: creative-arts.film-live-action.color-grading.matching-archive-stock-and-mixed-source-footage
name: matching-archive-stock-and-mixed-source-footage
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, colour-grading, film-live-action, archive-match, mixed-source-match, stock-match, archive-footage, stock-footage, rec-601, rec-709, deinterlace, upscaling, pillarbox, pulldown-removal, hlg, phone-footage, drone-footage, colour-space-transform, davinci-resolve]
level: practitioner
status: draft
description: "Grade archive, stock, phone and drone footage into a modern timeline: normalise colour space and cadence first, then decide how far to match versus keep the archive's character."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (Blackmagic - Colorist Guide to DaVinci Resolve, colour management and CST)"
  - "https://www.itu.int/rec/R-REC-BT.601 (ITU-R BT.601 - SD colour encoding)"
  - "https://www.itu.int/rec/R-REC-BT.709 (ITU-R BT.709 - HD colour encoding)"
  - "https://partnerhelp.netflixstudios.com/ (Netflix Partner Help Center - non-native and archival footage guidance)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Matching archive, stock and mixed-source footage

**Goal:** a documentary or drama mixing modern log camera footage with SD archive,
library stock, phone and drone clips plays as one film - without making the archive
look fake or the new footage look degraded.

## 1. Normalise before you grade
Fix the technical mismatches first; grading can't hide them.
- **Colour space per clip**: phone HDR (HLG / Dolby Vision HDR10) and drone log
  (D-Log, etc.) get the right input colour space or a **Color Space Transform** node to
  the timeline space. SD tape transfers are Rec.601; upconverted wrongly they shift
  greens/skin - use a 601-to-709 matrix conversion in the upscale.
- **Interlace**: deinterlace SD/1080i archive (Resolve *Clip Attributes > Enable
  deinterlacing*, or upstream in a converter) before scaling.
- **Cadence**: remove 3:2 pulldown from telecined film; convert 25/29.97 archive to the
  timeline rate with optical flow only where motion allows; keep a frame-blend or
  frame-repeat option for crowd shots that break optical flow.
- **Aspect**: 4:3 pillarboxed vs cropped is an editorial decision; get it signed off.
  Never stretch.
- **Legal range**: some archive arrives full-range or with crushed super-blacks; set
  data levels correctly in clip attributes.

## 2. Decide the match philosophy
- **Archive stays archive.** Audiences accept SD softness and old colour; they notice
  wrong white balance and jumps in black level. Match **black level, contrast range and
  overall exposure** to neighbours; keep the period colour.
- **Stock in a drama** must disappear: match fully - exposure, white balance, contrast
  curve, saturation, grain/sharpness to the hero camera.
- Phone and CCTV in documentary: correct exposure and neutralise heavy casts; keep the
  texture.

## 3. Practical matching
- Use the scopes: set blacks and whites to the hero shot's range on the waveform, then
  balance mid-grey on the parade, then skin on the vectorscope skin line.
- Sharpness and grain: soften over-sharp stock or phone clips slightly; add matched
  grain to the clean modern footage around archive if the film's look allows - this
  glues more than any colour move.
- Upscaled SD: mild noise reduction before the upscale, sharpening after, sparingly.

## Gotchas
- Restoring archive so heavily (NR + sharpening) it becomes waxy; worse than the
  original.
- Matching the archive's colour casts onto modern footage instead of the other way.
- Delivery specs (e.g. streamer limits on non-native/upscaled footage) - check the
  allowed percentage and document sources for QC.
- Burnt-in timecode or watermarks on screener-quality archive used in the online by
  mistake; conform must point to the licensed masters.

## Verify
- [ ] Every non-native clip has a known source colour space, frame rate and scan type.
- [ ] No cadence stutter or interlace combing on playback.
- [ ] Blacks/whites within the scene's range on the waveform.
- [ ] Archive masters, not screeners, in the final conform.
