---
id: creative-arts.film-live-action.davinci-resolve.clone-scene-detect-and-media-management
name: clone-scene-detect-and-media-management
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, clone-tool, resolve-offload, media-clone, scene-cut-detection-use, auto-scene-detect, split-flat-file, media-management-trim, consolidate-media, trim-media, checksum-offload]
level: practitioner
status: draft
description: "Use Resolve's media utilities: the Clone tool for verified offloads, Scene Cut Detector to split flat files, and Media Management to copy, move, trim or transcode a project's media."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Media page: Clone Tool, Scene Cut Detection; Media Management)"
  - "The Definitive Guide to DaVinci Resolve (Blackmagic official training) - media management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clone, scene detect and media management in Resolve

**Goal:** safe offloads, flat files split back into shots, and projects consolidated
for archive or handoff - all inside Resolve.

## 1. Clone tool (Media page)
1. Open the **Clone** palette (Media page toolbar).
2. **Add Job**; drag the camera card (source) onto the job, then add one or more
   **destinations** (two drives recommended).
3. Choose checksum (**MD5** or other offered options) in the job/ clone settings.
4. **Clone**: copies to all destinations and verifies against the checksum; job shows
   status. Keep the report/log.
For larger productions dedicated offload apps give richer reports, but Resolve's Clone is
verified and adequate for small shoots.

## 2. Scene Cut Detector (flat files)
For an exported single file of an edited programme (archive, an old master, a reference
cut) that needs re-grading:
1. Media page: right-click the clip > **Scene Cut Detection** (or in the Edit page via
   *Timeline > Detect Scene Cuts* on a clip in the timeline in newer versions).
2. **Auto Scene Detect** marks cuts; review the graph and threshold, add/remove cut
   points manually (detection fails on dissolves, flashes and fast motion).
3. **Add Cuts to Media Pool** -> clips per shot; or cut the timeline clip in place.
Now each shot can be graded separately.

## 3. Media Management (File > Media Management)
- **Copy** or **Move**: all media, or **timelines** only (media used in selected
  timelines).
- **Trim**: copy only the used portions of clips plus **handles** (e.g. 24-48 frames) -
  shrinks archives and handoffs drastically. Some formats (long GOP, some raw) can't be
  trimmed - Resolve may copy whole files or transcode.
- **Transcode**: render the used media to a new codec (e.g. ProRes) for handoff.
- Options: relink to the new media, preserve folder hierarchy, include render cache.
After running, open the new location in a test project to confirm everything relinks.

## Gotchas
- Wiping cards after a Clone job that showed a verification failure.
- Scene detection splitting on flashes and missing dissolves - always review.
- Trim with too-short handles; a later recut needs more.
- Media Management with "relink" on, unintentionally moving the live project to copies.

## Verify
- [ ] Clone jobs verified to two destinations; logs kept.
- [ ] Scene cuts reviewed manually before adding to the pool.
- [ ] Trimmed media has agreed handles; test relink confirmed.
- [ ] Live project's links intentional after media management.
