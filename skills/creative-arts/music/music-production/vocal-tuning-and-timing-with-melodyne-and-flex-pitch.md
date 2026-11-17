---
id: creative-arts.music.music-production.vocal-tuning-and-timing-with-melodyne-and-flex-pitch
name: vocal-tuning-and-timing-with-melodyne-and-flex-pitch
category: creative-arts
field: music
product: music-production
tags: [music-production, melodyne, flex-pitch, pitch-correction, auto-tune, vocal-tuning, pitch-drift, vibrato, formant, ara, timing-correction, vocal-editing, logic-pro, pro-tools]
level: practitioner
status: draft
description: "Tune and time vocals transparently with Melodyne (ARA) or Logic Flex Pitch: pitch centre, drift and vibrato, sibilants, formants, and Auto-Tune as an effect."
sources: ["https://helpcenter.celemony.com/ (Melodyne user manual)", "https://support.apple.com/guide/logicpro/edit-pitch-with-flex-pitch-lgcpa6fcee0c/mac", "https://www.antarestech.com/ (Auto-Tune Pro manual)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vocal tuning and timing (Melodyne, Flex Pitch)

**Goal:** an in-tune, in-time vocal that still sounds human (or a deliberate hard-tuned effect).

## 1. Before tuning
- Comp first; tune the final comp. Consolidate/bounce the comp so the tuning tool sees one region.
- Melodyne in Pro Tools/Logic/Studio One/Cubase via **ARA** (no transfer pass); in other DAWs, record into Melodyne.

## 2. Melodyne workflow
1. Check detection: algorithm "Melodic"; fix wrong note splits (Note Separation tool) and octave errors first.
2. **Pitch centre**: macro "Correct Pitch" at ~50-70% centre and 0-30% drift as a starting point, then go note by note.
3. Fix only what sounds wrong: long held notes off centre, sour notes in harmonies. Leave scoops and expressive slides.
4. **Pitch drift** tool: steadies wobble within a note without killing vibrato; **pitch modulation** scales vibrato depth.
5. **Timing**: move note starts or use Time tool; sibilants and breaths often detected as separate "notes" - don't tune them.
6. Formant tool for big pitch changes to keep tone natural.

## 3. Logic Flex Pitch
- Enable Flex (Cmd+F), choose Flex Pitch on the track; edit in the Track or Audio Track Editor. Each note has handles for pitch drift, fine pitch, gain, vibrato and formant shift. Right-click > "Set to Perfect Pitch" for selected notes (then reduce where unnatural).

## 4. Auto-Tune / real-time tuning as an effect
- Set key/scale; **retune speed** fast (0-10 ms) for the hard-tuned pop/trap sound; slower (20-50) for transparent correction. Humanize helps sustained notes.

## Gotchas
- Over-correcting every note: robotic, lifeless. Tune by ear in context.
- Tuning against the wrong reference (track tuned to A=442 or detuned instruments).
- Editing before the arrangement is final: later key changes require redoing.

## Verify
- Listen in context and solo: pitch sounds natural; no artefacts on consonants.
- Harmonies and doubles tuned to the lead rather than strictly to the grid where the lead bends.
