---
id: creative-arts.film-live-action.film-sound-design.remote-adr-sessions
name: remote-adr-sessions
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, sound-post, adr, remote-adr, source-connect, adr-remote, auto-restore, home-studio-kit, picture-streaming, talkback, adr-cueing, pro-tools-adr, local-recording]
level: practitioner
status: draft
description: "Run ADR with the actor in another city: Source-Connect links, a matched mic kit at the actor's end, picture streaming, beeps and local safety recordings that replace network dropouts."
sources:
  - "https://source-elements.com/products/source-connect/ (Source Elements - Source-Connect and Auto-Restore)"
  - "https://www.avid.com/pro-tools (Avid Pro Tools - ADR recording workflows)"
  - "https://www.mpse.org/ (Motion Picture Sound Editors - ADR craft)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote ADR sessions

**Goal:** lines recorded with the actor far away that cut in like stage ADR: in sync,
same mic colour, no network glitches, director and editor hearing and giving notes live.

## 1. Two ends, one session
- **Host stage** (you): Pro Tools session with the ADR cues, picture, guide track,
  beeps, recording tracks. Director, editor and ADR mixer listen here.
- **Remote end**: a partner ADR stage (best) or the actor's home/hotel kit.
- Link: **Source-Connect** (Standard/Pro) is the industry default; it streams
  high-quality audio both ways and, with **Auto-Restore**, records locally at the remote
  end and patches over any network dropouts afterwards.
- Picture to the actor: stream from the host (Source-Connect video sync, or a separate
  low-latency streaming tool) or send a watermarked local file and sync via timecode.

## 2. The remote kit
Match production as closely as possible:
- Same mic family as the boom (e.g. a shotgun like the MKH 416 or the show's model)
  plus the lav model if the scene was lav-heavy; interface with clean preamps;
  closed-back headphones (no beep bleed); a small, dead, quiet room or a vocal booth.
- Ship a pre-configured laptop if the actor isn't technical; have a local tech on site.
- Run a test day: level, room, latency, mic position photo.

## 3. Running it
- Latency: the actor hears beeps and guide on their end, so the recording is in sync
  locally; the host hears it delayed. Record the returned stream as a guide, then
  replace with the local (or Auto-Restored) files.
- Three-beep cueing as on stage; keep cue numbers spoken on talkback.
- Director gives notes over talkback; keep a single voice on talkback to avoid chaos.
- Slate each take with cue number and take into the file name/marker.

## 4. After
- Collect the remote end's local high-res files; conform them to the session by TC/markers.
- Note mic, room and distance per cue in the ADR log for the mixer.

## Gotchas
- Using only the streamed audio: compression artefacts and dropouts end up in the mix.
- Actor's room reverb (hotel bathroom tiles) - impossible to match; hang duvets, move rooms.
- Clock mismatch between ends (44.1 vs 48 kHz) - drift over long takes.
- Union/contract terms for remote sessions (equipment, technician, session fees) still apply.

## Verify
- [ ] Test session done with the actual kit and room.
- [ ] Local recordings collected and conformed for every circled take.
- [ ] Mic and room notes in the ADR log.
- [ ] Lines checked in context against production dialogue before releasing the actor.
