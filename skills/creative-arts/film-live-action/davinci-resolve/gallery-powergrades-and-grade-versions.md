---
id: creative-arts.film-live-action.davinci-resolve.gallery-powergrades-and-grade-versions
name: gallery-powergrades-and-grade-versions
category: creative-arts
field: film-live-action
product: davinci-resolve
tags: [davinci-resolve, resolve, film-live-action, powergrade, gallery-albums, stills-management, local-versions-use, remote-versions-use, grade-versions, reference-stills, split-screen-compare]
level: practitioner
status: draft
description: "Use the Gallery and grade versions in Resolve: grabbing and organising stills, PowerGrade albums across projects, comparing with wipes and split screen, and local vs remote versions."
sources:
  - "https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_Reference_Manual.pdf (Resolve Reference Manual - Gallery, PowerGrades, Local and Remote Versions)"
  - "The Colorist Guide to DaVinci Resolve (Blackmagic official training) - managing grades"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gallery, PowerGrades and grade versions

**Goal:** reference stills to match against, reusable looks across projects, and
alternative grades kept side by side for the client to choose.

## 1. Stills
- **Grab Still** (right-click viewer or `Ctrl/Cmd+Alt+G`): saves the frame and the grade
  (node tree) into the current Gallery album.
- Organise **albums** per scene ("Sc24 hero stills"), per reference ("Client refs"),
  per version. Label stills (right-click > change label).
- Import reference images (frames from refs) into an album for wipes.

## 2. Comparing
- Select a still and toggle **Image Wipe** (`Ctrl/Cmd+W`): wipe between the still and the
  current frame; wipe styles (horizontal, vertical, mix, alpha) in the viewer options.
- **Split Screen** (viewer option): view multiple clips or versions at once - selected
  clips, versions of the current clip, or album stills.
- Use stills of **hero shots** per scene to match every other shot of the scene.

## 3. PowerGrades
The **PowerGrade** album persists across all projects in the database: drag a still into
it to keep that grade available everywhere - show looks, node-tree templates (labelled
empty trees), utility setups (film looks, NR presets). Export stills as `.drx` (grade) +
image for sharing between databases.

## 4. Applying grades from stills
Right-click a still > **Apply Grade** (replace) or middle-click to apply; **Append Node
Graph** adds the still's nodes after the current ones. Apply to many selected clips at once.

## 5. Local vs remote versions
- **Local versions**: per-clip-instance grades - each timeline instance can be graded
  differently (default).
- **Remote versions**: grades linked to the **source clip** - every timeline using that
  clip gets the same grade (useful when the same media appears across versions of an
  edit, or across episodes from the same source). Switch per timeline in the clip's
  thumbnail context menu (*Use Remote Grades / Use Local Grades*).
- **Versions** (multiple grade versions on one clip): right-click thumbnail > Local/
  Remote Versions > Create New Version - keep "Day" vs "Dusk" options; switch to show the
  client.

## Gotchas
- Grabbing stills of unbalanced grades and matching to them.
- PowerGrade album cluttered - nobody finds anything; name and curate.
- Remote grades unintentionally changing other timelines.
- Forgetting which version was approved - label versions.

## Verify
- [ ] Hero stills grabbed per scene; albums organised and labelled.
- [ ] Wipes/split screens used to match.
- [ ] Show looks/templates saved as PowerGrades.
- [ ] Local/remote mode chosen deliberately; approved versions labelled.
