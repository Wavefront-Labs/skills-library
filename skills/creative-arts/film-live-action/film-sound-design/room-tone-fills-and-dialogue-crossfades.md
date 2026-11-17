---
id: creative-arts.film-live-action.film-sound-design.room-tone-fills-and-dialogue-crossfades
name: room-tone-fills-and-dialogue-crossfades
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, room-tone-filling, fill-editing, tone-fill, dialogue-crossfades, fade-shapes, edit-smoothing, alt-takes, production-alternates, dialogue-alt-takes, smooth-backgrounds]
level: practitioner
status: draft
description: "Smooth dialogue edits: building room-tone fills from production, crossfade lengths and shapes at cut points, and replacing words and lines from alternate takes."
sources:
  - "John Purcell, Dialogue Editing for Motion Pictures (fills, room tone, crossfades and alternate takes)"
  - "David Lewis Yewdall, Practical Art of Motion Picture Sound"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Room tone fills and dialogue crossfades

**Goal:** dialogue tracks where the background never jumps at a picture cut, every gap
is filled with the right tone, and bad words are replaced invisibly from other takes.

## 1. Fills (room tone)
- Every gap between lines (removed noises, cut picture, ADR holes) needs **fill** - room
  tone matching the surrounding production sound.
- Source fill from the **same take** first (pauses between lines), then the same set-up,
  then the scene's wild room tone recorded on set.
- Build fill by copying clean pauses and looping/ crossfading them; avoid audible repeats
  (vary pieces, crossfade 20-50 ms between pieces).
- Fill goes on the same track as the dialogue it supports (or the dedicated fill track
  per the house style) so the background is continuous under processing.

## 2. Crossfades at edits
- At every cut where background changes (different take/ set-up), use a **crossfade**
  long enough to smooth the background step - often **0.5-2 seconds** of overlapping tone
  (extend handles), with the dialogue itself not overlapping.
- Short fades (a few ms) at region boundaries inside words to prevent clicks.
- **Fade shapes**: equal-power for dissimilar backgrounds; equal-gain (linear) for
  correlated material (same take); S-curves for natural ramps.
- Background "bumps" at picture cuts are the most common amateur tell - listen with eyes
  closed.

## 3. Alternate takes (production alts)
- To fix a noisy word, a stumble or an overlap: find the same line in other takes (the
  editor's ScriptSync/ the sound reports help), **audition alternates**, and replace the
  word/ phrase, matching sync (align transients - plosives, consonants) and pitch/
  rhythm.
- Tools: manual sliding with elastic audio sparingly; VocAlign/ Revoice for sync matching.
- Replace with fill around the alt to match background.
- Prefer production alts over ADR - performance and room match.

## 4. Check
Solo each track and the whole dialogue bus; play through scene changes; watch picture for
sync on replaced words.

## Gotchas
- Looping a 1-second tone piece - audible pattern.
- Crossfades too short; background clicks/steps at cuts.
- Alt words out of sync by a frame on plosives.
- Fill from a different mic perspective - tone mismatch.

## Verify
- [ ] All gaps filled with matching tone; no repeats audible.
- [ ] Background-smoothing crossfades at every cut; no clicks.
- [ ] Alt-take replacements in sync and tonally matched.
- [ ] Whole-scene playback with eyes closed and with picture.
