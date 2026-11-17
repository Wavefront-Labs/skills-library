---
id: creative-arts.film-live-action.film-sound-design.adr-sessions-and-matching-to-production
name: adr-sessions-and-matching-to-production
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, post-production-sound, adr, automated-dialogue-replacement, looping, dubbing, adr-cue-sheet, adr-spotting, streamers, beeps, three-beeps, sync, lip-sync, vocalign, revoice-pro, mic-matching, room-matching, impulse-response, convolution-reverb, eq-matching, dialogue-editing, production-dialogue, walla, group-adr, pro-tools, re-recording-mix, adr-spotting-list, adr-cues, adr-stage, adr-mic-matching, adr-directing, adr-performance, sync-fitting, vocalign-use, adr-processing, adr-matching]
level: practitioner
status: draft
description: "Replace live-action dialogue that can't be saved: spotting and cue sheets, running the ADR session with beeps and streamers, mic and room matching, sync fitting, and cutting it into production."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ADR sessions and matching to production dialogue

**Goal:** when production dialogue is unusable (noise, distortion, an off-mic line, a
script change), record replacement lines in a studio and make them indistinguishable
from the production track in the final mix. For general dialogue-editing craft see
`creative-arts.animation.sound-design.dialogue-editing`; live-action ADR adds the hard
problem of matching an actor's on-set voice, space and lip movement.

## 1. Spotting: decide what really needs ADR
Try to save production first: alternate takes of the same line (from the ISO tracks or
other takes), wild lines, and noise reduction (e.g. iZotope RX or similar). ADR rarely
matches the original performance's energy. Spot the rest with the director/supervising
sound editor and record each line on an **ADR cue sheet**: cue number, character,
timecode in/out, the line as spoken (not as scripted), reason (noise, performance, story
change), and production mic notes (boom or lav, indoor/outdoor, distance).

## 2. Prep the session
- In Pro Tools (or similar), a session with picture, the production guide track, and
  each cue marked.
- **Cueing:** the actor gets audible **beeps** (commonly three beeps at one-second
  intervals, with the line starting where a fourth would fall) and/or visual
  **streamers** (a line sweeping across the picture ending at the start of the line).
  Agree the convention with the actor.
- Have the production clip ready to play in the headphones before each take.
- **Mic choice:** record with the **same type of mic** used on set (often the same model
  of boom mic at a similar distance and angle) plus, if the original was a lav, a lav
  placed similarly. Matching later is far easier when the source tonality is close.

## 3. Running the session
- Play the original 2–3 times; the actor repeats in rhythm, then records several takes.
- Watch for: **sync** (consonants and lip closures — b, p, m — landing on the picture),
  **energy and projection** (actors in a booth tend to speak too quietly; for an exterior
  shout they must actually shout, with physical movement if needed), **pitch** and pace.
- Record **efforts** too (breaths, grunts, reactions) when production ones are lost.
- Keep a take log per cue with circled takes and director's comments.
- Group ADR / **walla** (background crowd voices) can be recorded in the same block with
  a group of performers; give them specific context, not generic murmur.

## 4. Fitting and matching
1. **Sync fit:** cut the best take to sync by hand, or use a timing-alignment tool
   (e.g. VocALign or Revoice Pro) against the guide track; listen — automatic tools can
   produce artefacts on long stretches.
2. **EQ match** to the production dialogue around it (a short production line before and
   after is the reference). Studio recordings are cleaner and brighter; boom on location
   often has less low end and some room colour.
3. **Space:** add the location's acoustics with a convolution reverb (impulse response of
   a similar room) or a tuned algorithmic reverb; for exteriors, very little reverb but
   matching background.
4. **Fill:** lay production **room tone** / background under the ADR so the noise floor
   doesn't drop out at the line. Most "ADR sounds fake" problems are a missing noise floor.
5. **Checkerboard** ADR onto its own tracks in the dialogue edit so the re-recording mixer
   can treat it separately.

## Gotchas
- Replacing one line in a dialogue exchange where everything else is production — the
  mismatch jumps out. Sometimes replace the whole exchange instead.
- Perfect diction in ADR that the original performance didn't have.
- Forgetting legal/contract steps: actors' ADR availability and union rules vary by
  country; schedule ADR early (not confirmed in detail here).

## Verify
- [ ] Every cue has a reason, and alternates/noise reduction were tried first.
- [ ] Cue sheet with timecode, line as spoken and production mic notes.
- [ ] Same mic type/distance as production used in the session.
- [ ] Lines fitted to sync with no audible stretch artefacts.
- [ ] EQ, space and room tone matched; ADR on separate tracks for the mix.
- [ ] Played in context: the director can't pick which line is ADR.
