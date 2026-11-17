---
id: creative-arts.animation.editing.media-management-and-relinking
name: media-management-and-relinking
category: creative-arts
field: animation
product: editing
tags: [media-management, relink-media, consolidate, project-manager, offline-media, nle-project-setup, premiere-pro, resolve, avid, handles]
level: practitioner
status: draft
description: "Relink offline media, consolidate a cut with handles and hand off a self-contained project in Premiere, Resolve and Avid without losing shot versions."
sources:
  - https://helpx.adobe.com/premiere-pro/using/project-manager.html
  - https://helpx.adobe.com/premiere-pro/using/relinking-offline-media.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Media management and relinking

**Goal:** an editorial project that moves between machines, sites and vendors with every clip online and
pointing at the right shot version.

## Folder law

Media lives outside the project file in a fixed tree that mirrors production naming:
`<SHOW_ROOT>/editorial/media/<episode>/<sequence>/<shot>/<shot>_<dept>_v###.mov`. NLEs store absolute paths;
a predictable tree means one relink fixes the whole project (see
`creative-arts.animation.pipeline.cross-platform-path-mapping`).

## Relinking

- **Premiere:** select offline clips > right-click *Link Media*. Keep *Align Timecode* ticked when renders carry
  timecode; tick *Relink others automatically* so one find relinks the rest. Match on file name and extension and
  use *Search* on the root folder.
- **Resolve:** Media Pool > select clips > *Relink Selected Clips* (pick the root folder), or the relink icon above
  the Media Pool for all offline clips. Resolve matches by file name and timecode.
- **Avid:** select clips > Relink, by Source File Name or Tape/Source Name plus timecode; for linked (AMA) media use
  *Relink to file*.

## Consolidating for hand-off

- **Premiere:** File > Project Manager > *Collect Files and Copy to New Location* with *Exclude Unused Clips* and
  *Include Handles* (e.g. 12 frames). *Consolidate and Transcode* trims and renames files, which breaks
  round-trips to production versions; prefer Collect.
- **Resolve:** File > Media Management > *Timelines* > Copy, *Copy only used media* with handles.
- **Avid:** Consolidate (copy) with handles, keep master clips linked.

## Animation specifics

Shot versions replace each other constantly. Keep the version number in the file name and use *Replace Footage*
(Premiere) or *Replace Selected Clip* (Resolve) so the timeline clip keeps its edits while pointing at v004
instead of v003; check frame counts first, because a v004 of different length shifts the tail of the shot.

## Verify

Open the consolidated project on another machine with the source drive unplugged: zero offline clips, and the
timeline plays with correct version burn-ins (see `creative-arts.animation.editorial.review-burn-ins`).
