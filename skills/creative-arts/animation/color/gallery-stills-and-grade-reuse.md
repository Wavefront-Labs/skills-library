---
id: creative-arts.animation.color.gallery-stills-and-grade-reuse
name: gallery-stills-and-grade-reuse
category: creative-arts
field: animation
product: color
tags: [gallery-stills, gallery, grade-reuse, powergrade, drx, shot-matching, resolve, look-and-matching]
level: practitioner
status: draft
description: "Use Resolve's Gallery for reference stills, split-screen matching and reusing grades across shots and episodes with stills, PowerGrades and DRX files."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gallery stills and grade reuse

**Goal:** match shots to approved references and reuse grades without regrading.

## Stills

- Grab a still: right-click the viewer > *Grab Still* (Ctrl/Cmd+Alt+G). A still stores the image **and** its grade.
- Label stills (shot code, approved date). Organise in albums per sequence.
- **Compare:** select a still and enable *Image Wipe* (Ctrl/Cmd+W); set wipe mode (horizontal, vertical, mix) or
  split screen with several stills.

## Applying a grade from a still

- Right-click the still > *Apply Grade* replaces the current grade.
- Middle-click on the still (with a clip selected) applies its grade to the clip; with several clips selected it
  applies to all.
- *Append Node Graph* adds the still's nodes after the current ones.

## PowerGrades (cross-project)

PowerGrade albums are shared across all projects in the database. Save the show's empty node tree, sequence looks
and episode reference grades there so episode 5 reuses episode 1's looks.

## DRX files (cross-database)

Right-click a still > *Export* writes the image and a `.drx` grade file. Import into another system's gallery to
share grades with a vendor or another colourist. Keep DRX exports in the show's colour folder in version control.

## Animation workflow

1. Grade the sequence's hero shot with the director.
2. Grab still, label "SQ020 HERO approved".
3. Apply to all shots in the sequence, then match each with the wipe and parade
   (`creative-arts.animation.color.rgb-parade-balancing`).
4. At the end of the episode, save hero stills to PowerGrades for the series.

## Verify

Opening a new episode project, the PowerGrade album lists the series references, and applying one to a matching
shot reproduces the approved look (wipe shows no visible difference on neutrals).
