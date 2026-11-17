---
id: creative-arts.animation.pipeline.annotations-and-note-capture
name: annotations-and-note-capture
category: creative-arts
field: animation
product: pipeline
tags: [annotations, note-capture, review-notes, frame-notes, openrv, kitsu, shotgrid-notes]
level: practitioner
status: draft
description: "Capture review notes that artists can act on: frame-specific annotations, text notes tied to versions, note structure, export and sync with the tracker."
sources:
  - https://aswf-openrv.readthedocs.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Annotation and note capture

Notes are the output of review. A note that cannot be acted on, or is lost, costs a retake.

## What a good note has
- **Where**: the shot, the **version**, and the **frame or time**. A drawing over the frame removes ambiguity.
- **What**: the change, as an observation or direction ("the arm reads late on the turn", "shadow too hard under the chin"). Prefer describing the problem plus intent.
- **Priority**: must-fix versus nice-to-have.
- **Who**: the author and the person responsible.

## Capture
- Annotate on the frame in the review player: OpenRV, tracker review tools and web review services support drawing and text on frames. Notes are stored per version and frame.
- A scribe records spoken notes in the tracker live (`dailies-review.md`), or annotations are exported afterwards.
- Link notes to the **tracker entity**: ShotGrid Notes are linked to Versions and tasks; Kitsu comments belong to tasks and previews (`production-tracking.md`).
- Keep the **frame rate** correct so a frame number refers to the same frame in every tool (`remote-review-timecoded-notes.md`).

## Export and sync
- Export notes as a PDF or CSV for people who do not use the tracker, with thumbnails of the annotated frames.
- Sync into the tracker with scripts (`shotgrid-python-api.md`, `kitsu-and-gazu.md`) where the player and the tracker are separate.
- Keep **one source of truth**: the tracker. Do not let notes live in emails.

## Closing the loop
1. Artist reads notes, marks each as addressed with a short reply.
2. New version references the previous version's notes.
3. Reviewer checks off notes, not just watches the new version.

## Verify
- [ ] Every note has shot, version and frame or time.
- [ ] Notes sit in the tracker.
- [ ] Next review checks the previous notes.
