---
id: creative-arts.music.music-production.programming-drums-velocity-swing-humanising
name: programming-drums-velocity-swing-humanising
category: creative-arts
field: music
product: music-production
tags: [music-production, beatmaking, sound-design, drum-programming, humanising, velocity, swing, groove-quantize, mpc-swing, ghost-notes, hi-hat-programming, drum-machine, step-sequencer, piano-roll, hip-hop-drums]
level: practitioner
status: draft
description: "Program drums that groove: velocity patterns, swing amounts, micro-timing per instrument, hi-hat and ghost-note programming, and avoiding the machine-gun effect."
sources: ["https://www.ableton.com/en/live-manual/12/using-grooves/", "https://support.apple.com/guide/logicpro/ (Drummer and Step Sequencer)", "https://www.akaipro.com/ (MPC user guide - swing and note repeat)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Programming drums: velocity, swing, humanising

**Goal:** programmed drums that feel played, in any style.

## 1. Start with a real drummer's logic
- A drummer has two hands and two feet: don't program hi-hat and two other hand hits at the same instant unless it's a flam or a crash on a kick.
- Learn the genre's core pattern by ear (transcribe a reference loop).

## 2. Velocity
- Hi-hats: accent pattern - downbeats ~100-110, off-beats ~70-85 (8ths), or 16ths cycling 110/60/85/60.
- Snare backbeats consistent and strong (~110-127); **ghost notes** on 16ths at 25-50.
- Kick: main hits strong; pickup kicks a bit softer.
- Use sample libraries with **velocity layers and round robins** so repeated hits don't sound identical.

## 3. Timing and swing
- **Swing** delays every second 16th (or 8th). MPC-style swing ~54-58% is "slight", 62-66% heavy (MPC 50% = straight, 66% = triplet).
- Apply swing per instrument: hats swung, kick and snare straighter, for a lazy feel.
- **Micro-timing** (by ms): snare slightly late (+5-15 ms) for laid-back hip-hop/neo-soul (Dilla-style unquantised); kick on grid; hats ahead for urgency in rock/punk.
- Groove templates: extract from a reference loop (Ableton Extract Groove, Logic Groove Track) and apply to MIDI.

## 4. Humanising tools
- Random velocity (+/- 5-10) and timing (+/- 5 ms) as a base - subtle; then edit by hand where it matters.
- Better: **play it in** on pads and quantise partially (50-75% strength) instead of 100%.
- Vary the pattern every 4 or 8 bars: an open hat, a ghost-note change, a fill.

## 5. Genre starting points
| Genre | Tempo | Notes |
|---|---|---|
| Boom bap | 85-95 | swung 16ths, punchy kick and snare, sample chops |
| Trap | 130-150 (half-time feel) | 808, hat rolls (1/32, triplets) with pitch/velocity ramps, snare/clap on 3 |
| House | 120-128 | four-on-the-floor kick, off-beat open hat, claps on 2 and 4 |
| Drum and bass | 170-175 | two-step breakbeat, chopped breaks |

## Gotchas
- 100% quantise + fixed velocity = machine gun; acceptable only as a deliberate electronic aesthetic.
- Hats too loud: the most common programming flaw; they dominate the feel.

## Verify
- Loop 8 bars and listen without looking: does it make you nod?
- Compare against a reference track at matched level for hat/snare balance and feel.
