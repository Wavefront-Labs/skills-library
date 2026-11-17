---
id: creative-arts.film-live-action.davinci-resolve.fairlight-adr-and-foley-sampler
name: fairlight-adr-and-foley-sampler
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, fairlight-adr, adr-tool, adr-cue-list, foley-sampler-use, sound-library, fairlight-sound-library, beeps-and-streamers, cue-import]
level: practitioner
status: draft
description: "Record ADR with Fairlight's ADR tool (cue lists, beeps, streamers, takes, ratings) and perform/edit foley with the Foley Sampler and the Fairlight sound library."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Fairlight: ADR, Foley Sampler, Sound Library)"
  - "The Fairlight Audio Guide to DaVinci Resolve (Blackmagic official training)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fairlight ADR and the foley sampler

**Goal:** run ADR and foley sessions inside Resolve without leaving the timeline.

## 1. ADR tool setup
Fairlight page > **ADR** panel (toolbar). Tabs: **List**, **Record**, **Setup**.
- **Setup**: record track(s) and input, **pre-roll/ post-roll**, **beeps** (three beeps
  before the cue start, the fourth "silent beep" is where the actor starts), video
  **streamer/cue overlay** shown to the actor on the video output, guide track selection.
- **List**: create cues manually (mark in/out on the timeline, character, dialogue text)
  or **import a cue list** (CSV in the supported format). Each cue has number, TC in/out,
  character, line.

## 2. Recording
- Select a cue; actor hears the beeps and the guide (original production line) in
  headphones; watches the streamer on the video monitor.
- Record takes; each take lands on the record track as a layered take; **rate** takes
  (stars) and mark the **favourite**. Resolve keeps all takes (layered audio) for
  comping.
- Record with the same mic and room as the rest of the session; note mic distance.
- Export the cue list/takes report for the dialogue editor.

## 3. Foley Sampler
A sampler instrument (Fairlight FX) loaded on a track: load samples (footsteps per
surface, cloth, props), map them to pads/keys, and **perform** to picture with a MIDI
keyboard or pad - velocity controls dynamics, round-robin variations avoid repetition.
Record the performance as audio on the track, then edit sync.

## 4. Sound library
The **Sound Library** panel indexes your SFX folders (and the free Fairlight library
download): scan folders, search by name/metadata, audition, drag to the timeline. Keep
the database on shared storage for teams.

## 5. Practical notes
- ADR in Resolve suits indie/doc work; large features use Pro Tools with EdiCue/ADR
  Studio-type tools - export AAF if the mix moves elsewhere.
- Keep picture locked or use change lists; cue TCs depend on it.

## Gotchas
- Pre-roll too short for the actor to get in rhythm.
- Guide track muted in the actor's headphones (or too loud and bleeding into the mic).
- Takes overwritten because layered recording was off.
- Foley sampler with one sample per surface - machine-gun repetition.

## Verify
- [ ] ADR setup: beeps, streamer, pre/post-roll, guide and record tracks.
- [ ] Cue list imported/created with characters and lines.
- [ ] Takes layered, rated and favourites marked; report exported.
- [ ] Foley sampler loaded with variations; performances edited to sync.
