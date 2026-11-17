---
id: creative-arts.animation.pipeline.review-playlists-and-dailies
name: review-playlists-and-dailies
category: creative-arts
field: animation
product: pipeline
tags: [review-playlist, playlists, dailies, openrv, review-session, version-ordering, production-tracking]
level: practitioner
status: draft
description: "Build review playlists for dailies and client reviews: choosing versions, ordering, matching colour and burn-ins, OpenRV sessions and tracker playlists, closing the loop."
sources:
  - https://aswf-openrv.readthedocs.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Review playlists

A **playlist** is an ordered set of shot versions prepared for a review session. A good one makes the review fast and produces clear decisions (`dailies-review.md`, `sweatbox-director-review.md`).

## Build it
1. **Select the right versions**: the latest version of each shot in the pipeline step under review, not older ones. Tracker queries can build this automatically.
2. **Order by purpose**: story order (sequence/shot) for continuity reviews, or by department, or hard shots first; order by the reviewer's priority.
3. **Include context**: previous version for comparison where the note was "fix X", and reference (animatic or story reel) for timing.
4. **Consistent media**: same resolution, frame rate, colour space and burn-ins (`review-burn-ins.md`), and the audio synced (`video-track-sync-in-the-daw.md`).
5. **Name and date** it: `EP01_anim_2026-10-18`.

## Tools
- **OpenRV** (open-source review player; ASWF project) works with sessions and sequences; playlists in many trackers launch it. It supports frame-accurate comparison (wipes, A/B), colour management and annotation (`annotations-and-note-capture.md`).
- **ShotGrid** has a Playlist entity and can launch RV; **Kitsu** has playlists for dailies and build-your-own lists; other trackers have the same idea.
- For media players that play files, make a **concatenated movie** with burned-in shot names (`image-sequence-encode.md`) as a fallback.

## During and after
- Record decisions on each shot: approved, final with notes, retake (`annotations-and-note-capture.md`).
- Update statuses in the tracker immediately after the session (`production-tracking.md`).
- Archive the playlist so you can show what was reviewed and when.

## Gotchas
- Mixed colour spaces make shots look inconsistent: normalise through the review colour pipeline.
- Playlists built by hand drift from the tracker; prefer auto-built lists.

## Verify
- [ ] Each entry is the intended version.
- [ ] Media matches in format and colour.
- [ ] Statuses updated after review.
