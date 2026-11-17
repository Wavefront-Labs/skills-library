---
id: creative-arts.theatre.theatre-sound-design.dca-programming-for-musical-mixing
name: dca-programming-for-musical-mixing
category: creative-arts
field: theatre
product: theatre-sound-design
tags: [theatre, theatre-sound-design, mixing-a-musical, line-by-line-mixing, dca-programming, dca, vca, console-scenes, scene-recall, script-mixing, digico, yamaha, pit-mixing]
level: practitioner
status: draft
description: "Mix a musical line by line: DCA assignments per scene, console scenes and recall safes, the mixing script, opening only the mics that speak, and balancing the band."
sources:
  - "https://digico.biz/"
  - "https://usa.yamaha.com/products/proaudio/mixers/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DCA programming for musical mixing

**Line-by-line mixing**: the operator opens a performer's mic for each line
they sing/speak and closes it after, so only the active voices are live —
reducing noise, comb filtering and feedback. Standard in West End/Broadway
musicals.

## DCA (VCA) programming
- **DCA** faders control groups of input channels without passing audio.
- In each **console scene** (cue), assign the speaking/singing actors to DCAs
  in a logical layout — e.g. DCA 1-8 for the principals in that scene, in
  stage-left-to-right or entrance order; DCA 9-10 band/vocals.
- The operator then mixes on a fixed set of 8-12 DCA faders while the mic
  inputs underneath change scene by scene.
- Label DCAs with character names per scene (consoles show scribble strips).

## Scenes and recall
- Each scene stores DCA assignments, mutes, effects sends, and possibly EQ/
  routing per actor (e.g. different wig = different EQ).
- Use **recall safe/scope** so scene recalls don't overwrite things you want
  live (e.g. band levels).
- Scenes advance by the operator's GO (or by MIDI/OSC from QLab/Eos).
- Typical shows: hundreds of scenes.

## The mixing script
- Script marked with scene numbers and DCA layout per page; when each mic
  opens/closes; who sings which line in ensembles.
- Practice "following the script" until muscle memory takes over.

## Band and pit mixing
- Band on separate DCAs/groups; balance band to vocals per number; use
  automation sparingly; drummer in a booth or screened if needed.
- Talkback with the MD; click/foldback routing for the band.

## Gotchas
- Opening mics late (clipping first syllables) or too early (breath/noise).
- Two actors' mics open in close proximity → comb filtering; open only one in
  duets standing close.
- Scene recall overwriting the band mix.

## Verify
- [ ] Every scene has labelled DCA assignments.
- [ ] Recall safes set for band and FX returns.
- [ ] Mixing script marked and practised against a recording of a run.
