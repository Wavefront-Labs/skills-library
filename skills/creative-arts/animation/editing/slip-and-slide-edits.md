---
id: creative-arts.animation.editing.slip-and-slide-edits
name: slip-and-slide-edits
category: creative-arts
field: animation
product: editing
tags: [slip-slide, slip-edit, slide-edit, trimming, trim-tools, premiere-pro, resolve, avid, handles]
level: practitioner
status: draft
description: "Use slip and slide edits to change which frames of a shot play, or move a shot along the cut, without changing sequence length, in Premiere, Resolve, Avid."
sources:
  - https://helpx.adobe.com/premiere-pro/using/trimming-clips.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Slip and slide edits

**Goal:** adjust timing inside a shot (slip) or shift a shot between its neighbours (slide) with the total cut
length unchanged.

| Edit | What moves | What stays |
|---|---|---|
| Slip | the clip's source in and out points move together | clip position, duration, neighbours |
| Slide | the clip moves along the timeline; outgoing neighbour's out and incoming neighbour's in adjust | clip content and duration, sequence length |

## Tools

- **Premiere:** Slip tool **Y**, Slide tool **U**. With a clip selected, Alt/Option+Left/Right slips one frame and
  Alt/Option+Comma/Period slides one frame. The Program monitor shows a four-up (neighbour edges and new in/out)
  while dragging.
- **Resolve:** Trim Edit mode **T**; drag the clip's name bar to slide and the clip body to slip; comma and period
  nudge one frame.
- **Avid:** in Trim mode, select the head and tail edits of the clip on opposite sides for a slip; use Segment
  mode with Slide for a slide.

## Animation use

- **Slip** when an animator's take has the right length but the director wants the action to start a few frames
  later in it, e.g. lose a held anticipation. Only possible if the shot was rendered with **handles**; many
  animation shots have none, so editorial requests extra frames through a change list
  (`creative-arts.animation.editorial.editorial-change-lists`).
- **Slide** repositions a cutaway or insert relative to dialogue without retiming the reel.

## Gotchas

- Slipping a clip with linked audio slips the dialogue too and breaks lip-sync. Unlink first or lock the audio tracks.
- The slip stops at the media edge when source frames run out; check the four-up display rather than assuming
  the full move happened.

## Verify

After a slip the timecode of the following edit is unchanged; after a slide the total duration is unchanged and
only the two neighbouring edit points moved. Related: `creative-arts.animation.editing.ripple-roll-trims`.
