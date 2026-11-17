---
id: creative-arts.music.ableton-live.scale-mode-and-key-awareness
name: scale-mode-and-key-awareness
category: creative-arts
field: music
product: ableton-live
tags: [ableton-live, ableton, live-12, live-midi-editing, scale-mode, scale-awareness, root-note, fold-to-scale, highlight-scale, clip-scale, transpose-in-key, fit-to-scale]
level: practitioner
status: docs-checked
description: "Use Live 12 Scale Mode: set root and scale per clip, highlight and fold the piano roll to scale, fit notes to scale and use scale degrees for transpose and invert."
sources:
  - https://www.ableton.com/en/live-manual/12/editing-midi/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scale mode and key awareness (Live 12)

**Goal:** keep MIDI writing in key and make scale-based edits quickly.

## 1. Setting the scale
- Toggle **Scale Mode** with the button in the Main Clip Properties panel in Clip View, or in the Control Bar.
- The **Root Note** and **Scale Name** choosers set the root and scale for the selected clip(s). The scale belongs to each clip, so a clip can carry its own key.
- With several clips of different scales selected, the foreground clip's scale applies to newly created clips.

## 2. Piano roll features
- **Highlight Scale** (button in the Clip View header) highlights the key tracks in the chosen scale; highlighting is applied globally.
- **Fold to Scale** (available only when a scale is active) hides key tracks outside the scale. **Fold to Notes** hides key tracks with no notes. Notes already outside the scale stay visible.
- **Fit to Scale** moves notes to the nearest scale degree.
- The **Transpose** slider uses scale degrees when a clip scale is active, and so does Invert. Intervals can be set in scale degrees.
- Up and down arrow keys transpose selected notes; hold Shift to transpose by octaves.
- The Find and Select Notes Scale filter has a Use Clip Scale toggle.

## 3. Workflow
1. Set the root and scale on the clips at the start.
2. For a modulation section, set that clip's scale separately.
3. Use Fold to Scale while writing melodies, then turn it off to add deliberate chromatic notes.

## Gotchas
- Imported MIDI clips may not carry the intended scale; set it.
- Scale-degree transposition changes interval quality on some degrees; check chords afterwards.

## Verify
- With Scale Mode on, Fit to Scale moves out-of-scale notes onto highlighted rows.

## Checked
2026-11-01. Confirmed in the Live 12 manual, Editing MIDI (Pitch and Time Utilities, Find and Select Notes, Folding and Scales): Scale Mode toggle, Root Note and Scale Name choosers, foreground-clip rule, Highlight Scale, Fold to Scale vs Fold to Notes, Fit to Scale, Transpose and Invert by scale degree, Shift+arrow octave transposition, Use Clip Scale filter. Removed: global scale selector, arrow keys moving by scale degree, MIDI Tools/device "Use Current Scale" option, Scale device, Push scale link and scale-name list (not stated on the page).
Method: documentation only; no commands were run.
