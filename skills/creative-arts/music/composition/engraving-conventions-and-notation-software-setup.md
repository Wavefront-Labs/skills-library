---
id: creative-arts.music.composition.engraving-conventions-and-notation-software-setup
name: engraving-conventions-and-notation-software-setup
category: creative-arts
field: music
product: composition
tags: [composition, arranging, pitch-notation, music-notation, engraving, notation-software, part-preparation, dorico, sibelius, musescore, finale, part-extraction, cue-notes, page-turns, rehearsal-marks, score-layout]
level: practitioner
status: draft
description: "Set up a score and extract professional parts in Dorico, Sibelius or MuseScore: layout, rehearsal marks, cues, page turns, multirests and the engraving checks players expect."
sources: ["Elaine Gould, Behind Bars (Faber, 2011)", "https://www.steinberg.help/dorico_pro/", "https://www.avid.com/sibelius", "https://musescore.org/en/handbook/4", "https://mola-inc.org/ (Major Orchestra Librarians' Association guidelines for music preparation)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Engraving conventions and part preparation

**Goal:** a full score that a conductor can read and parts that players can sight-read in
a session without a single question.

## 1. Score setup
- Instrument order (orchestral): woodwinds, brass, percussion, keyboards/harp, soloists/voices, strings. Big band: saxes, trumpets, trombones, rhythm.
- Score at **concert pitch** for film/session and most modern scores (state "Score in C"); transposed for traditional orchestral publishing.
- Staff size: score 4-5 mm for A3/tabloid; parts **7 mm** (Gould) on A4 or 9x12 in.
- Title, composer, instrumentation list, tempo and metronome mark on page 1.

## 2. Part essentials
1. **Rehearsal marks** (letters or bar numbers in boxes) every 8-16 bars at phrase starts; bar numbers at every system start.
2. **Multirests** with the count; long rests broken at rehearsal marks and meter/key changes.
3. **Cue notes** (small, with instrument name) after long rests (8+ bars) before an exposed entry.
4. **Page turns**: put a rest of a few bars at the bottom right of odd pages; use "V.S." (volti subito) only as a last resort.
5. Courtesy accidentals and courtesy key/time signatures at system ends.
6. Dynamics on every entry, including after rests; hairpins end on a target dynamic.
7. Tempo text and metronome marks at every change, repeated in every part.

## 3. Software workflow (applies to Dorico, Sibelius, MuseScore)
- Enter at concert pitch; let the program transpose parts.
- Use the program's **layout** objects, not manual drags: system/frame breaks, part-only properties (Dorico "part layout" scope; Sibelius parts tab; MuseScore "Parts" dialog).
- Set house style once (fonts, staff size, multirest style) and save as a template.
- Before export: run checks for collisions, hidden objects, notes out of range (Dorico colours out-of-range notes; Sibelius plug-in "Check Pitch Ranges"; MuseScore colours out-of-range notes red).
- Export PDF parts with the title, part name and page numbers in the header.

## Gotchas
- Manually nudged objects break when layout changes; reset positions before final export.
- Copy-pasted dynamics that are score-only don't appear in parts (check the scope).
- Swing feel: write "Swing" text, don't notate dotted rhythms everywhere.
- Repeats and D.S./Coda make parts shorter but cause sight-reading errors in sessions; studio work usually writes everything out.

## Verify
- Print one part and sight-read it (or ask a player): any hesitation marks a fix.
- Check every part's first page shows instrument, transposition and tempo.
- Bar count in every part equals the score.
