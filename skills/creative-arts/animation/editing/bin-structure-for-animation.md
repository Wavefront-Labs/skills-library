---
id: creative-arts.animation.editing.bin-structure-for-animation
name: bin-structure-for-animation
category: creative-arts
field: animation
product: editing
tags: [bin-structure, nle-project-setup, nle, bins, naming-conventions, editorial-organisation, premiere-pro, resolve, avid]
level: practitioner
status: draft
description: "Organise NLE bins and clip names for an animation series so any editor finds the boards, layout, animation and final versions of a shot in seconds."
sources:
  - https://helpx.adobe.com/premiere-pro/using/organizing-assets-project-panel.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://developer.adobe.com/premiere-pro/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bin structure for an animation show

**Goal:** a project layout identical across episodes, so assistants load turnovers by script and editors never
search.

## Template (one per episode, copied from a master project)

```
00_SEQUENCES      cut_v###, animatic_v###, lock, deliverables
01_BOARDS         by sequence (sq010, sq020 ...)
02_LAYOUT         by sequence, one clip per shot version
03_ANIMATION      by sequence (blocking, splined, final)
04_LIGHTING_COMP  by sequence
05_AUDIO          scratch_vo, final_vo, temp_music, temp_sfx, mix_stems
06_GFX            titles, slates, leaders, cards
07_REFERENCE      reference clips, previous episode lock
99_ARCHIVE        superseded sequences (never delete in-season)
```

## Naming

- Clips carry the shot code and version: `ep104_sq020_sh0040_anim_v007`. Sort order then equals story order.
- Sequences are versioned and dated: `ep104_cut_v012_2026-10-16`. Duplicate before every major change; never
  overwrite a cut that was screened.
- Use metadata columns (Premiere *Description*, Resolve *Comments*, Avid custom columns) for status rather than
  renaming clips.

## Making it automatic

Turnover and ingest scripts should create the bin path from the shot code, e.g. Resolve's scripting API
`MediaPool.AddSubFolder(parent, name)` per sequence, or Premiere ExtendScript `app.project.rootItem.createBin(name)`.
Hand-built bins are where drift begins.

## Gotchas

- Smart bins and search bins (Premiere search bins, Resolve Smart Bins, Avid custom sifts) are useful *latest
  version* views but are not folder structure; keep the real bins too.
- Avid bins are individual files; in shared projects a bin is locked by whoever opened it first, so give each
  editor their own working bins.

## Verify

A new assistant, given only a shot code and department, finds the clip in under 10 seconds, and the same bin path
exists in every episode project.
