---
id: creative-arts.animation.pipeline.synchronised-remote-review
name: synchronised-remote-review
category: creative-arts
field: animation
product: pipeline
tags: [sync-review, remote-review, cinesync, synchronized-review, frame-accurate, review-tools, video-conference]
level: practitioner
status: draft
description: "Run synchronised remote reviews: local-media sync tools versus screen sharing, frame accuracy, colour and audio, host control, note capture and security."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Synchronised remote review

Remote reviews need everyone to see the same frame at the same moment. There are two broad approaches.

## 1. Synchronised local playback
- Each participant loads the same media on their own machine, and the tool keeps playback position, annotations and zoom in step across the participants. Products built for this include cineSync (now offered by Backlight), SyncSketch and RV-based setups; available features and ownership change, so check the vendors' current documentation.
- **Advantages**: frame-accurate stepping, full quality (no video-conference compression), local colour management.
- **Needs**: media pre-delivered to each participant, identical versions, and clear naming.

## 2. Screen sharing / video call
- Easy and universal, but the video is **re-compressed, colour-shifted and may drop frames**, so it is unreliable for fine animation or colour judgement. Use it for story and rough work, not final polish.
- Many tools only share the frame rate of the call.

## Running a session
1. Send the playlist media in advance (`review-playlists-and-dailies.md`), through secure channels (`secure-file-transfer-and-screeners.md`).
2. Check each participant's **display and colour setup** matches the requirement for the kind of review (`grading-viewing-environment.md`).
3. Agree a **host** who controls playback; others annotate or request control.
4. Use a separate voice channel (call) for talking and the sync tool for picture.
5. A **scribe** captures notes in the tracker (`annotations-and-note-capture.md`).
6. Check audio sync and the playback frame rate at the start with a test clip.

## Gotchas
- Different media versions on different machines is the most common failure: check the version names and checksums.
- Time zones: set recurring slots and give notes in writing afterwards.
- Do not leave an unwatermarked cut on personal computers longer than needed.

## Verify
- [ ] Everyone loaded the same media version.
- [ ] Frame stepping lines up on all machines.
- [ ] Notes recorded in the tracker.
