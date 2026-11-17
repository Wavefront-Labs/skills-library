---
id: creative-arts.film-live-action.film-sound-design.composer-delivery-score-stems-and-mix
name: composer-delivery-score-stems-and-mix
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, music-editing, composer-delivery, score-stems-use, score-mix, score-stems, music-stems, cue-naming, score-mixer, music-editor, stem-null-test, tempo-map, music-delivery-spec]
level: practitioner
status: draft
description: "Specify and receive composer delivery: score stem layout, file naming and start times, mix format, the score mix stage, null-testing stems and what the music editor needs for the dub."
sources:
  - "https://www.mpse.org/ (Motion Picture Sound Editors - music editing)"
  - "https://www.themusiceditor.com/ (The Music Editor - film music editing practice)"
  - "Richard Davis, Complete Guide to Film Scoring (Berklee Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Composer delivery, score stems and the score mix

**Goal:** every score cue arrives in the mix room in sync, in the mix format, split
into stems the re-recording mixer can balance, with names that tell everyone what and
where it is.

## 1. Write the delivery spec early
Send the composer (and score mixer) a spec at spotting time:
- **Format**: 48 kHz, 24-bit (or the show's 32-bit float), WAV/BWF, with
  timecode-stamped start; mix width (stereo, 5.1, 7.1, Atmos bed/objects).
- **Stem layout**, e.g. Strings, Brass, Woodwinds, Percussion, Synths/Electronics,
  Choir, Solo/Featured, Low end; plus the full mix.
- **Naming**: `1M03_TheChase_v4_STRINGS_7.1.wav` (reel/cue number, title, version,
  stem, format).
- **Start**: every stem starts at the same timecode (the cue's start or a common
  head), same length, including tails/reverb ring-out.
- Tempo map/click and session (Pro Tools/Logic) for the music editor; cue sheet data
  (title, composer, publisher, timings).

## 2. Stem rules
- **Stems must sum to the full mix**: no bus compression/limiting on the full mix that
  isn't applied in the stems. Null-test: stems summed minus mix = silence (or near).
- Reverbs printed into the stem they belong to.
- Don't split a stem by a single instrument unless asked; too many stems slows the dub.
- Keep headroom; no final limiter on score stems.

## 3. Score mix
- The score mixer mixes from the recording/mockup into stems at the mix format,
  listening against the dialogue/temp mix where possible so the score leaves room for
  dialogue frequencies in dialogue-heavy cues.
- Revisions after picture changes: composer delivers updated cues with a new version
  number; music editor conforms.

## 4. Music editor intake
- Check every file: sample rate, length, TC start, naming, stem count.
- Lay stems in the MX tracks at timecode; confirm sync against the composer's
  reference QuickTime; flag clicks, missing tails and level jumps.
- Keep a delivery log: cue, version, date received, issues.

## Gotchas
- Stems that don't null because of mix-bus processing.
- Files bounced from "bar 1" with no TC - every cue hand-synced.
- Version numbers reused for different content.
- 44.1 kHz deliveries in a 48 kHz show: drift and resampling artefacts.

## Verify
- [ ] Delivery spec sent before scoring starts.
- [ ] Stems null against the full mix for every cue.
- [ ] Every file named, timestamped and logged.
- [ ] Sync confirmed against the composer's reference video.
