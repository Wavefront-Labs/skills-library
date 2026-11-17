---
id: creative-arts.animation.editing.editorial-version-control-and-conform
name: editorial-version-control-and-conform
category: creative-arts
field: animation
product: editing
tags: [conform, edl, xml, aaf, cut-versioning, locked-cut, reel-naming, online-offline, otio, opentimelineio, premiere, resolve, avid, reconform, picture-lock, handles]
level: practitioner
status: draft
description: "Name, track and conform cut versions across EDL/XML/AAF round-trips so a locked edit survives updated media without drift."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Editorial Version Control and Conform

**Goal: when picture locks, make sure every later swap of underlying media (an
updated render, a re-recorded VO line, a color pass) lands back in the exact cut
without re-introducing a timing or sync bug.** This is distinct from
`creative-arts.animation.editing.animatic-assembly` (which builds the cut in the first
place by concatenating per-shot clips to a scripted duration) and from
`creative-arts.animation.editing.dialogue-and-action-timing-splices` (where inside a
clip the splice falls) — this skill is about **what happens after a cut is declared
locked**: naming versions so nobody edits the wrong one, and round-tripping an edit's
structure (not its pixels) between tools or back from updated source media.

## Versioning the cut itself

- **Never overwrite a locked version file.** Save each state as a new file:
  `EP01_v07_locked.prproj` / `.drp` / `.aaf`, not `EP01_final_FINAL2.prproj`. The
  version number is the single source of truth for "which decisions are baked in" —
  if two people have different v-numbers open, their notes are talking about different
  cuts.
- **Freeze a cut by exporting its structure, not just saving the project.** An EDL
  (Edit Decision List), XML (Final Cut/Premiere interchange), or AAF (Avid, carries
  more metadata) is a plain-text/binary record of every clip, in/out point and
  transition — independent of the authoring tool's project format, which can corrupt
  or become unopenable after an app update. Export one alongside every locked version.
- **Tag the lock, not just the date.** A commit-style note per version ("v07: picture
  lock pending VFX shot 040 placeholder, sound not mixed") travels with the file far
  better than a filename date — reviewers need to know what's still a placeholder in
  a "locked" cut, since picture lock and sound lock usually land at different times.

## Conform: bringing updated media into a locked structure

Conform means re-linking a locked edit's timeline to new/updated media **without
changing the edit decisions**:

- **Match by reel/clip name and timecode, not by file path.** Editorial conform tools
  (Avid's "Consolidate/Transcode," Resolve's "Conform from Bin," relinking in
  Premiere) find the next version of a clip by its reel name + source timecode
  range, so an updated render must preserve the **same clip name and source
  timecode** as the one it replaces, or the conform silently drops the shot instead
  of swapping it.
- **Carry handles.** Request/render a few extra frames of **handle** (typically 8-12)
  on each side of a locked clip's in/out so a later trim adjustment or retime doesn't
  run out of source frames — a cut with zero handle can't nudge a splice without
  re-rendering.
- **Reconform after a reorder breaks sync.** If anyone reorders or ripple-trims the
  locked timeline (even briefly, to preview an alternate), re-export the EDL/XML
  afterward and diff shot order against the locked reference before calling the cut
  "still locked" — a ripple trim upstream silently shifts every downstream clip's
  recorded timecode, which an inattentive roll-back won't necessarily restore exactly.
- **OpenTimelineIO (`otio`) is the modern lossless bridge** between NLEs that don't
  share a native project format (e.g. Resolve <-> a custom in-house pipeline) — prefer
  it over EDL when transitions, markers or nested sequences matter, since EDL cannot
  represent most of those; fall back to EDL only for the simplest cut-list hand-off.

## Gotchas

- **Frame rate mismatches break conform silently.** An EDL/XML carries timecode, not
  absolute time; swapping in media authored at a different fps (23.976 vs 24 vs 25)
  shifts every downstream cut point by a few frames per minute, cumulative and
  invisible until something's noticeably out of sync downstream.
- **AAF handles audio and video sync separately.** A conform that relinks picture but
  not the matching audio essence (or vice versa) can look right in the first few
  seconds and drift over a long reel — spot-check sync at the end of a long reel, not
  just the head.
- **Don't conform onto a project file someone still has open.** Binary project
  formats (Premiere `.prproj`, Avid bins) can silently discard another person's
  unsaved conform if two people conform the same sequence at once — lock or
  communicate before a conform pass, the same discipline as not editing a shared file
  concurrently.

## Verify

- [ ] The locked version has an exported EDL/XML/AAF alongside the project file, not
      just an autosave.
- [ ] Every clip in the conform target matches by reel name + source timecode, not by
      guessing from a renamed file.
- [ ] Handle frames exist on both sides of every clip (check in the bin/media pool,
      not just the timeline) before trims are attempted.
- [ ] After any reorder/trim done "to preview," the timeline was diffed against the
      last locked EDL/XML before being called locked again.
- [ ] Audio and picture sync both checked at the **end** of a reel after conform, not
      only the first few shots.

Status: draft — conform/reconform discipline described here is standard NLE practice
(Avid/Resolve/Premiere interchange via EDL/XML/AAF/OTIO); not yet verified against a
specific in-house conform script the way `animatic-assembly`'s ffmpeg recipe was. If a
project uses a scripted (non-NLE) conform step, record its exact tool/flags here
rather than opening a competing skill.
