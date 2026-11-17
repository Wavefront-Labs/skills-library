---
id: creative-arts.animation.voice-tts.reading-dialogue-onto-an-exposure-sheet
name: reading-dialogue-onto-an-exposure-sheet
category: creative-arts
field: animation
product: voice-tts
tags: [x-sheet, exposure-sheet, dope-sheet, lip-sync, track-reading, dialogue-breakdown, timing]
level: practitioner
status: draft
description: "Read a dialogue track onto an exposure sheet: frame-by-frame breakdown, marking accents, choosing mouth shapes, holding rules and handing over to the animator."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Reading dialogue onto an exposure sheet

The exposure sheet (X-sheet, dope sheet) is a grid with one row per frame and columns for dialogue, action, drawings and camera. In 2D production a track reader (or the animator) breaks the dialogue down on it. Modern software (Toon Boom Harmony, Animate, TVPaint) includes a sound-scrub view with the same purpose.

## Method
1. Load the final or approved scratch track at the project frame rate (usually 24 fps; see `timecode-drop-frame.md` for fractional rates).
2. Scrub frame by frame and write the **word and syllable** starts in the dialogue column.
3. Mark the **accents** (stressed syllables): they get the strongest, most open shapes.
4. For each syllable choose the viseme (`mouth-chart-and-viseme-set-design.md`). Vowels carry the shape; consonants usually only matter when visible, such as closed M, B, P and the F, V lip-on-teeth shape.
5. **Closures** (M, B, P) must be drawn as a closed mouth on or just before the frame where the sound starts; the audience notices a missing closure more than anything else.
6. **Hold** each shape at least 2 frames at 24 fps in most styles; a flicker of single frames can read as noise. Hold the final vowel of a phrase until the sound ends, then close or rest.
7. Many animators place the mouth shape a frame or two ahead of the sound so the picture appears in sync, as the picture generally needs to lead the sound perceptually; check this against your show's convention and fix by review (`lip-sync-review-and-offset-correction.md`).
8. Add head accents and eye blinks on the beats in the action column so the body supports the dialogue.

## Handover
- Output the X-sheet as PDF or software-native timing; the animator keeps the dialogue rows locked.
- When the track changes, re-read only the changed lines and note the revision.

## Verify
- [ ] Each stressed syllable has a clearly open shape.
- [ ] Every M, B, P is closed on the sound start.
- [ ] Shapes hold at least 2 frames, except fast words where deliberate.
