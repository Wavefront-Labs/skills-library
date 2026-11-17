---
id: creative-arts.film-live-action.davinci-resolve.project-setup-media-page-and-collaboration
name: project-setup-media-page-and-collaboration
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, media-page, project-settings, project-library, project-libraries, resolve-database, postgresql, blackmagic-cloud, collaboration, collaborative-workflow, multi-user, bin-locking, optimized-media, optimised-media, proxy-media, proxy-generation, render-cache, smart-cache, timeline-resolution, timeline-frame-rate, media-pool, smart-bins, metadata, clip-attributes, scene-cut-detection, relink, media-storage, cache-location, project-backup, drp, archive-project, master-settings, image-scaling, master-settings-detail, project-preset, media-pool-bins, smart-bins-setup, metadata-editor, resolve-proxies, optimised-media-generation, proxy-mode, database-backup, postgresql-setup, project-library-management, multi-user-collaboration, bin-locking-workflow, cloud-project, proxy-sync]
level: practitioner
status: draft
description: "Set a Resolve project up right: project libraries (local, PostgreSQL, Blackmagic Cloud), master settings, Media page import and smart bins, proxies vs optimised media, multi-user collaboration."
sources:
  - "https://www.blackmagicdesign.com/products/davinciresolve/training (The Definitive Guide to DaVinci Resolve - Media page, project settings, collaboration chapters)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Project setup, Media page and collaboration in Resolve

**Goal:** a project whose frame rate and storage are correct from the first clip, whose
media is organised for a long edit, and which several people can work in at once
without overwriting each other.

## 1. Project libraries (databases)
Open the **Project Manager** (home icon) > *Project Libraries* panel:
- **Local** (disk database) for a single machine. Back up by *Export Project Library*
  (`.resolve.diskdb`) or per-project `.drp` (`File > Export Project`).
- **Network (PostgreSQL)** for a facility: one shared library on a server; required for
  classic collaboration. Needs the PostgreSQL installer from Blackmagic.
- **Blackmagic Cloud**: cloud-hosted project library (paid per library) usable from
  anywhere; media stays local and syncs via *Blackmagic Cloud Store* or Dropbox/
  LucidLink paths with **Proxy Generator** proxies - collaboration without a server.
Name libraries by show; never keep a year of shows in one local library (it gets slow and
one corruption takes all).

## 2. Master settings (set before importing)
`File > Project Settings > Master Settings`:
- **Timeline frame rate** - cannot be changed once a clip is in the Media Pool. 23.976 /
  24 / 25 / 29.97 to match camera/project. Playback frame rate follows.
- **Timeline resolution** (UHD 3840x2160, 2K DCI, etc.) - changeable later, but set
  for the deliverable; use *Timeline Format > Mismatched resolution: Scale entire image to fit*.
- **Optimized media** format (ProRes 422 Proxy / DNxHR LB for speed; ProRes 422 HQ for
  quality), **Render cache** format, **Cache files location** on a fast drive (the
  *Working folders* section).
- **Color Management** (Colour Science: DaVinci YRGB vs YRGB Color Managed; see the
  node-tree skill) - set now, as grades depend on it.
- *Image Scaling*: default *Scale entire image to fit*; sharper/bicubic for upscales.
Use **Presets** to save the show's settings (`Project Settings > Presets > Save As`)
and apply to every episode/reel project.

## 3. Media page
- **Media Storage** browser: add the media volumes (right-click > *Add New Location*)
  so Resolve indexes them and relinks fast.
- Import by dragging to the **Media Pool** (bins); *Create bin per folder* on drag
  keeps camera roll structure. Camera RAW shows decode settings in *Camera RAW* panel.
- **Clip Attributes** (right-click): fix frame rate (e.g. a 50 fps clip meant for 25),
  audio channel mapping (mono ISOs vs stereo), alpha, timecode, anamorphic **PAR**.
- **Metadata** panel: Scene/Shot/Take/Camera/Keywords - fill from ALE import
  (`Media Pool > Import > Metadata from file`) or by hand; drives **Smart Bins** (rules
  like `Scene = 12` or `Keyword contains interview`) which auto-populate.
- **Sync audio**: select clips > right-click > *Auto Sync Audio > Based on Timecode /
  Waveform*; choose *Append tracks* to keep camera scratch.
- **Scene Cut Detection** for flattened masters you must re-edit (right-click clip).
- Power bins (shared across projects) for logos, leaders, LUT clips.

## 4. Proxies, optimised media, caches
- **Proxy media** (Resolve 17+): right-click > *Generate Proxy Media* or use the
  **Blackmagic Proxy Generator** app watching a folder; proxies live beside originals in
  a `Proxy` folder and toggle via `Playback > Proxy Handling > Prefer Proxies`. Best
  for remote/cloud collaboration.
- **Optimized media**: right-click > *Generate Optimized Media* - stored in the cache
  folder, used automatically when `Playback > Use Optimized Media If Available`. Best
  for heavy RAW on one workstation.
- **Render cache**: `Playback > Render Cache > Smart/User`; caches Fusion and heavy
  colour nodes. Clear old caches (`Playback > Delete Render Cache`) when swapping drives.
- Link/relink: `Media Pool > right-click > Relink Selected Clips` to a folder; *Unlink*
  and *Replace Selected Clip* for a single swap; **Reconform from Bins** for timelines.

## 5. Collaboration
- Enable in `File > Project Settings > Collaboration > Multiple user collaboration` on
  a PostgreSQL or Cloud library. Users then open the same project; **bin and timeline
  locking** is automatic (a lock icon shows who holds it); *Chat* panel; edits/grades
  from others appear via the refresh icon.
- Typical roles: editor owns the timeline, colourist works in the same timeline's colour
  (grades are per clip, not locked with the timeline), assistant populates bins, sound
  edits in Fairlight on the same timeline - Resolve merges per-page work.
- Everyone needs the same media paths (identical mount names/drive letters) or uses
  *Mapped Mount* in `Preferences > Media Storage`.

## 6. Backups
`Preferences > User > Project Save and Load`: enable **Live Save** and **Project
Backups** (every 10 min / hourly / daily to a backup folder). Export `.drp` at
milestones; `.dra` archives (`Export Project Archive`) bundle media for handoff.

## Gotchas
- Frame rate set wrong, discovered after cutting: the only fix is a new project and a copy-paste of the timeline (timecodes shift).
- Cache folder on the system drive filling it mid-edit.
- Optimised media left behind when moving to another machine (it's in the cache, not next to the media).
- Collaboration on a local library - two people, two divergent projects.
- Audio channel mapping unchecked: ISO track 3 is silent in the edit for a week.

## Verify
- [ ] Library type chosen for the team; master frame rate and resolution set before import.
- [ ] Media Storage locations added; metadata populated; smart bins working.
- [ ] Proxy or optimised strategy chosen and tested on the slowest machine.
- [ ] Collaboration enabled with matching mounts; backups and `.drp` exports scheduled.
