---
id: creative-arts.film-live-action.film-sound-design.dialogue-session-setup-and-splitting
name: dialogue-session-setup-and-splitting
category: creative-arts
field: film-live-action
product: film-sound-design
tags: [film-sound-design, film-live-action, dialogue-session, dialogue-track-layout, dx-tracks, track-splitting, splitting-by-mic, perspective-split, dialogue-editing, aaf-import, pro-tools-dialogue]
level: practitioner
status: draft
description: "Set up a dialogue editing session from the picture AAF and split dialogue onto tracks by character, mic and perspective so the mixer can treat each consistently."
sources:
  - "John Purcell, Dialogue Editing for Motion Pictures (session setup and splitting tracks)"
  - "David Lewis Yewdall, Practical Art of Motion Picture Sound (dialogue editorial)"
  - "https://www.avid.com/pro-tools (Avid Pro Tools - AAF import and session data)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dialogue session setup and splitting

**Goal:** a dialogue session where every region sits on a track that groups sounds
needing the same processing - so the mixer sets EQ/ NR once per track, not per clip.

## 1. Build the session
- Import the editor's **AAF** (with handles - ideally 5+ seconds) into Pro Tools; relink
  to production **poly WAVs** (all iso tracks, not just the mix) - conform tools such as
  EdiLoad, Conformalizer or Pro Tools' Field Recorder workflow (*Field Recorder
  Channel Expansion/ alternate channels*) pull iso tracks matched by timecode and metadata.
- Reference picture with burn-in TC and a 2-pop; session at 48 kHz/24-bit, frame rate
  matching picture.
- Template: dialogue tracks (e.g. 8-16 DX tracks), PFX tracks, ADR tracks, X/ junk track,
  room tone/ fill tracks; colours per group; a dialogue bus/ stem.

## 2. Track layout logic (Purcell)
Split so that **each track holds sound with consistent character**:
- By **mic**: boom on one set of tracks, each actor's lav on its own.
- By **perspective/ set-up**: a wide-angle boom sounds different from a close one - split
  so the mixer can EQ them separately.
- By **character** where mics match.
- By **location/scene**: alternate scenes across track groups ("checkerboarding") so
  scene changes don't sit on the same track - easy to treat each scene independently.
- Problem/ to-be-fixed regions to a dedicated track.

## 3. Choosing mic per line
Audition boom vs lav for every line: prefer the boom for natural perspective; use lav
where the boom is off-axis, noisy or missing; avoid summing both unless aligned (phase).
Remove the unused mic's region (or mute) - don't leave both playing.

## 4. Organise for the mix
- Name tracks clearly (`DX1 BOOM`, `DX3 LAV MARTA`), consistent across reels.
- Markers for issues (ADR candidates, noise, missing tone).
- Keep production effects worth saving (footsteps, door) for the PFX tracks.

## Gotchas
- Working only from the editor's mix track - iso mics never relinked.
- Boom and lav both left playing - phasing.
- Same track used for adjacent scenes with different tones - mixer can't treat separately.
- Short handles in the AAF; no room for fades and fills.

## Verify
- [ ] AAF imported with handles; iso channels relinked.
- [ ] Track template with DX/PFX/ADR/fill groups.
- [ ] Regions split by mic, perspective and scene.
- [ ] Mic choice made per line; issues marked.
