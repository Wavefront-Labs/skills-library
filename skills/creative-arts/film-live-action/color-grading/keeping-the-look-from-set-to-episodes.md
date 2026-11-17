---
id: creative-arts.film-live-action.color-grading.keeping-the-look-from-set-to-episodes
name: keeping-the-look-from-set-to-episodes
category: creative-arts
field: film-live-action
product: color-grading
tags: [color-grading, film-live-action, look-to-set, look-to-dailies, lut-distribution, look-consistency, episodic-look, series-look, reel-matching, cdl-pipeline, grade-copying, append-node, ripple-grade]
level: practitioner
status: draft
description: "Keep a look consistent: distributing LUTs and CDLs to set and dailies, copying and rippling grades in Resolve, and matching across reels and episodes of a series."
sources:
  - "https://theasc.com/asc (ASC - Color Decision List)"
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - copying grades, ripple, groups, ColorTrace)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping the look from set to episodes

**Goal:** the look the DP approved on set is what editorial watches, what the client
approves, and what every reel and episode delivers.

## 1. Look to set and dailies
- Distribute the **show LUT** (and neutral variant) to: camera monitoring (load into
  camera/ LUT boxes), DIT (Livegrade), dailies lab, VFX. Version-control it; announce
  changes with a memo and dates.
- On set, per-scene adjustments are **CDLs** (slope/offset/power/sat) applied before the
  show LUT; DIT saves them per clip; dailies apply the same CDL + LUT so editorial sees the
  set look.
- Provide the final grade team the CDLs as a starting point (imported via EDL/ALE/ CDL
  files in Resolve).

## 2. Copying grades efficiently (Resolve)
- **Middle-click** a thumbnail to copy its grade to the current clip; `=` applies the
  previous clip's grade; **Append node graph** to add on top.
- **Ripple** (*Color > Ripple Node Changes* or via the Gallery/ copy options): propagate a
  change made on one clip to others that share the setup (by exact values or by
  relative change).
- **Shared nodes** and **group grades** (pre-clip/post-clip) for a scene - change once,
  everything updates.
- **ColorTrace** to transfer grades from an old timeline version to a new edit when the
  cut changes.

## 3. Across reels and episodes
- Keep a **look template project** with timeline nodes, groups and PowerGrades for the
  show; each episode starts from it.
- **Hero stills** per location/character in a shared Gallery album; match new episodes
  against them with wipes/split screen.
- Grade episodes in order where possible; revisit the first after the last (the look
  drifts while you work).
- Same display, calibration and ambient conditions each session; recalibrate monitors on
  schedule.

## 4. Reel and episode QC
Watch reel/episode transitions back-to-back; compare skin and black levels of recurring
locations across episodes; keep a log of look changes approved mid-season.

## Gotchas
- A LUT update reaching set but not dailies (or vice versa).
- Rippling absolute values to clips that needed relative tweaks.
- Look drift across a season; episode 8 warmer than episode 1.
- Uncalibrated monitors in different suites for the same show.

## Verify
- [ ] Show LUT versions distributed and logged; CDLs flow from set to dailies to grade.
- [ ] Grades copied/rippled/grouped efficiently; ColorTrace used on recuts.
- [ ] Look template and hero stills shared across episodes.
- [ ] Cross-episode comparisons done; calibration consistent.
