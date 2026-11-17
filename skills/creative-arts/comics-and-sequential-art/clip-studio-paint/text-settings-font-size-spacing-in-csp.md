---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.text-settings-font-size-spacing-in-csp
name: text-settings-font-size-spacing-in-csp
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-text-tool, csp-balloons, csp-text-settings, font-size, line-spacing, character-spacing]
level: practitioner
status: draft
description: "Set up comic text in Clip Studio Paint: font, size, alignment, line and character spacing, anti-aliasing, edge, per-character edits and saving a lettering text sub tool."
sources:
  - https://blambot.com/pages/comic-book-grammar-tradition
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Text settings (font, size, spacing)

## Core settings (Text tool > Tool property / Sub Tool Detail)
- **Font** and **Size** (pt or the unit set in Preferences > Ruler/Unit; set text unit consistently).
- **Style** (bold/italic simulation), **Alignment** (centre for balloons), **Direction** (horizontal or
  vertical).
- **Line spacing** (leading) and **character spacing** (tracking) under Sub Tool Detail > Font/Text or
  the text palette depending on version.
- **Anti-aliasing** - turn off or set "none" for crisp monochrome print text at 600 dpi only if the
  publisher wants hard-edged bitmap text; otherwise keep it on for colour/screen.
- **Edge** (border) for text over art with no balloon (white outline around SFX or captions).

## Per-character edits
- Select characters in a text layer and change size/colour/font for emphasis (bold italic stressed word)
  without splitting the layer.

## Lettering presets
1. Duplicate the Text sub tool (Sub tool palette menu > Duplicate sub tool).
2. Set your dialogue font, size, centre alignment, spacing.
3. Name it ("Dialogue 9pt"), and make others ("Caption", "Whisper", "Shout").
4. Export them (.sut) for other machines or assistants.

## Sizing guide
- US comic pages at print size: dialogue roughly 7-9 pt in a comic lettering font; check publisher spec.
- Webtoon 800 px canvas: see mobile legibility guidance, about 22-30 px.

## Gotchas
- Fonts missing on another computer get substituted when the file opens; convert to raster or share fonts
  (licences permitting) before handing off.
- Faux bold on lettering fonts looks heavy; use the font's real bold.

## Verify
- [ ] All balloons use the preset sub tools; size consistent across pages.
