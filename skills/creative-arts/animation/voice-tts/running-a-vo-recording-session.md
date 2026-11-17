---
id: creative-arts.animation.voice-tts.running-a-vo-recording-session
name: running-a-vo-recording-session
category: creative-arts
field: animation
product: voice-tts
tags: [recording-session, vo-recording, voice-over, adr, session-management, animation-voice]
level: practitioner
status: draft
description: "Run an animation voice-over session: pre-session prep, slate and wild lines, direction flow, pickups, safeties and end-of-session delivery of takes with notes."
sources:
  - https://elevenlabs.io/docs
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Running a voice recording session

An animation VO session is usually one actor, one director, one engineer, often with a producer or writer listening remotely. The job is to leave with every line performed at least twice with usable variety, labelled so editorial never has to guess.

## Before the day
- Send the actor the script pages for their scenes, character sheet, and a line count a few days ahead. Pages for the session should be the locked or latest approved draft with a revision colour or date on every page.
- Prepare the session file: sample rate and bit depth agreed with editorial (48 kHz / 24-bit is the common film/TV standard; confirm with the show), one track per actor, a clean track plus a scratch/guide track if needed, markers per line ID.
- Decide the recording order. Common practice is to record in script order for continuity of emotion for scene-driven shows, or by emotional intensity (shouting last) to protect the voice.
- Have water (room temperature), a quiet script stand, and a headphone mix with a little actor-side reverb only if the actor asks for it.

## In the room
1. **Slate**: engineer or director states show, episode, session date, actor and character on the first take of the session. Each take is then announced with the line ID/page number so that the DAW markers match the log.
2. **Room tone**: record 30 seconds of silence in the booth at the start. It is handy for later gap filling and noise profiling.
3. **Warm-up take** on a mid-intensity line to set level. Set gain so loud peaks stay well below clipping; do not rely on limiters in the record path.
4. **Direction**: give one note at a time, as a playable action ("more tired", "like you just got caught"), not a line reading unless the actor asks for one. Give the actor the context of the shot or animatic when possible.
5. **Alts and wild lines**: after the scripted line, record a looser alternate, then wild lines (reactions, efforts, breaths, laughs) separately from dialogue so editors can cut them in later.
6. **Pickups**: record pickup lines when a performance starts to drift or a word is clipped. Stay on the same mic and distance as the original session where possible so pickups match.
7. **Safeties**: before the actor leaves, play back anything the director is unsure about. It is far cheaper than recalling the actor.

## After the session
- Save the session, then export the takes as unprocessed WAV per line using the naming scheme in `vo-file-naming.md`, plus the take log (see `take-logging-and-circle-takes.md`).
- Back up to two locations before wiping local storage.
- Send a short session report: lines done, lines missed, lines flagged for re-record.

## Gotchas
- Cloth, jewellery, and stomach noises show up on close mics: ask the actor to remove them before the first take.
- Do not process the record (compression, EQ) beyond a high-pass filter if the mic chain needs one; leave the dialogue editor room.
- Remote sessions through a call tool should still record locally at the actor end (or at the studio via a source-connect style service) rather than capturing the call audio.

## Verify
- [ ] Each take has a slate or marker with line ID.
- [ ] Peaks stay clear of clipping and a room tone file exists.
- [ ] Take log and exported WAVs are backed up in two places.
