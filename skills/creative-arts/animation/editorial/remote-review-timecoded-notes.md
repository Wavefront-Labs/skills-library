---
id: creative-arts.animation.editorial.remote-review-timecoded-notes
name: remote-review-timecoded-notes
category: creative-arts
field: animation
product: editorial
tags: [remote-review, review-approval, cut-review, frame-io, timecoded-notes, review-links, comment-export, nle-markers, client-review]
level: practitioner
status: draft
description: "Run remote cut reviews with timecoded comments (Frame.io-style), control link permissions, and bring notes back into the NLE as markers for fast fixes."
sources:
  - https://help.frame.io/en/
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Remote review with timecoded notes

**Goal:** directors, producers and clients who are not in the room give precise, frame-accurate notes that
the editor can act on directly.

## Setup

- Upload the review cut (H.264 with burn-ins, `creative-arts.animation.editorial.review-burn-ins`) to the
  review platform (Frame.io, ftrack Review, ShotGrid, Kitsu, Vimeo review).
- Create a review link per audience: set expiry, disable downloads for external viewers, require login or
  passphrase, enable watermarking for external links (`creative-arts.animation.pipeline.forensic-watermarking`).
- Version stacks: upload v012 onto v011 so reviewers can compare and comments stay organised per version.

## Asking for useful notes

- Send a short brief with the link: what to review (timing of sq020, not colour), the deadline, and that
  comments should be placed on the frame they refer to.
- Encourage drawing tools for framing and staging notes.

## Bringing notes into the edit

- Frame.io integrates with Premiere Pro, Resolve, FCP and Avid via panels/integrations: comments appear as
  timeline markers at their timecodes.
- Without integration: export comments as CSV/XML from the platform and import as markers (Resolve: Timeline -
  Import - Timeline markers from EDL; or convert CSV to an EDL with marker comments).
- Resolve's built-in collaboration and Blackmagic Cloud also support remote review with timeline comments.

## Workflow

1. Editor triages comments: mark each as do, discuss, or no (with a reply).
2. Fix, upload new version to the stack, reply "done in v013" on each comment.
3. Resolve comments only when the reviewer confirms (or per agreed rules).

## Gotchas

- Timecode offsets: if the upload starts at 00:00:00:00 but the timeline starts at 01:00:00:00, markers land
  1 hour off; set the start timecode on the platform or offset on import.
- Mobile reviewers on poor connections see low-res proxies; ask for critical image notes on desktop.

## Verify

After import, markers land on the frames the reviewers commented on (check two by eye), and the comment list
shows every note answered for the new version.
