---
id: creative-arts.animation.editorial.as-broadcast-dialogue-list
name: as-broadcast-dialogue-list
category: creative-arts
field: animation
product: editorial
tags: [dialogue-list, continuity-script, as-broadcast-script, combined-continuity, deliverables, localisation, dubbing, picture-lock]
level: practitioner
status: draft
description: "Produce the as-broadcast continuity and dialogue list from the locked cut: per-line timecodes, speakers, on-screen text and music, ready for dubbing and subtitles."
sources:
  - https://partnerhelp.netflixstudios.com/hc/en-us
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# As-broadcast continuity and dialogue list

**Goal:** a document that describes the locked programme exactly as delivered, line by line, so dubbing studios,
subtitlers and legal can work without the edit project.

## Contents (per event, in timecode order)

| Field | Example |
|---|---|
| Event / shot number | 0042 |
| Timecode in / out | 01:03:12:05 - 01:03:14:20 |
| Speaker | MIA (OS) |
| Dialogue verbatim, as performed (not as scripted) | "You said you'd be here by ten." |
| On-screen text / graphics | sign: "CLOSED" |
| Music cue | 1M04 "Night Drive" (see cue sheet) |
| Notes | overlapping dialogue, sung line, foreign language line (forced subtitle) |

Netflix calls this deliverable a dialogue list (combined continuity and dialogue in some territories); check its
current template and whether it wants spotting at the subtitle-event level.

## Method

1. Start from the final script, not the shooting script; in animation the VO record often changed lines.
2. Transcribe against the **final mix**, not the scratch: ad-libs, cut words and walla that is intelligible all count.
3. Timecode each line from the locked timeline; an automated first pass via forced alignment
   (see `creative-arts.animation.voice-tts.forced-alignment-of-dialogue`) saves hours, then check by ear.
4. Mark speaker conventions: (OS) off-screen, (VO) voice-over, (CONT'D), (SINGING).
5. Add on-screen text and music cue references that need translation or clearance.

## Uses downstream

Dub script adaptation (`creative-arts.animation.voice-tts.dub-script-adaptation`), SDH and subtitles
(`creative-arts.animation.encode-delivery.subtitles-captions`), music cue sheets, and compliance review.

## Verify

Spot-check 20 random lines against the master: speaker, words and timecode in/out within one frame of the audio.
