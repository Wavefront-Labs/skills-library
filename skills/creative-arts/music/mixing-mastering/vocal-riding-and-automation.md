---
id: creative-arts.music.mixing-mastering.vocal-riding-and-automation
name: vocal-riding-and-automation
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, mix-automation, vocal-riding, vocal-automation, clip-gain, fader-rides, vocal-rider, word-level-automation, breath-editing, automation-modes, touch, latch]
level: practitioner
status: draft
description: "Ride a lead vocal so every word is audible: clip-gain pre-levelling, fader automation passes, word-level fixes, breath handling and when a vocal-rider plugin helps."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. Mixing with Automation", "https://www.waves.com/plugins/vocal-rider (Vocal Rider manual)", "https://support.apple.com/guide/logicpro/ (automation modes)", "https://www.avid.com/pro-tools (Pro Tools automation)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vocal riding and automation

**Goal:** the lead vocal sits at a consistent perceived level against the track, line by line
and word by word.

## 1. Pre-level with clip gain (before compression)
- Use clip/region gain to even out big differences (quiet verses vs belted choruses, single loud or soft words) so the compressor sees a steadier signal. Aim for phrases within a few dB of each other.

## 2. Compression then automation
- Compress for tone and control (see compressor settings skill), then automate **after** compression (post-insert fader automation) to keep the vocal in front of the changing arrangement.

## 3. Fader passes
1. Loop a section; put the fader in **Touch** (returns to previous value when released) or **Latch** (stays where you leave it).
2. Ride by ear against the track: push up word ends that drop, pull down loud syllables, lift lines where the arrangement gets dense.
3. Second pass for detail; then edit breakpoints with the pencil for single words.
- Typical moves: 1-3 dB. Bigger moves usually mean a clip-gain or arrangement fix is needed.

## 4. Word-level and detail fixes
- Consonants: lift soft "t", "k" ends; reduce harsh "s" with de-essing or clip gain on the sibilant itself.
- Breaths: reduce by 6-12 dB rather than deleting (deleted breaths sound unnatural), except in dense pop where silence can work.
- Automate reverb/delay sends for throws on specific words (see delay throws skill).

## 5. Vocal rider plugins
- Waves Vocal Rider and similar ride gain automatically relative to the music (sidechain the instrumental bus). Write their moves to automation, then fix by hand. Useful for speed; not a replacement for listening.

## Gotchas
- Automating before compression and EQ are settled: changes to inserts alter the needed rides.
- Riding in Write mode overwrites everything; use Touch/Latch.
- Over-riding into a flat, lifeless vocal: keep the singer's dynamics where they're expressive.

## Verify
- Listen at low volume: every word should be intelligible.
- Mute and unmute the automation (bypass) on a chorus: the automated version sits more consistently.
