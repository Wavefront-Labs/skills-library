---
id: creative-arts.animation.editing.nested-sequences-and-compound-clips
name: nested-sequences-and-compound-clips
category: creative-arts
field: animation
product: editing
tags: [nested-sequences, compound-clips, nest, edit-effects, premiere-pro, resolve, avid, conform, edl]
level: practitioner
status: draft
description: "Nest sequences and build compound clips to group a split screen or a multi-layer shot, and un-nest before EDL/AAF export so the conform does not break."
sources:
  - https://helpx.adobe.com/premiere-pro/using/nesting-sequences.html
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nested sequences and compound clips

**Goal:** treat several clips as one object in the cut (apply one effect, trim as one, reuse a sequence) without
breaking interchange.

## How

- **Premiere:** select clips > right-click *Nest...* (creates a sequence in the bin and puts it on the timeline).
  Toggle *Insert and overwrite sequences as nests or individual clips* in the timeline header to control whether
  dropping a sequence nests it or expands its clips.
- **Resolve:** select clips > right-click *New Compound Clip*; *Decompose in Place* reverses it. Use
  *Open in Timeline* to edit inside.
- **Avid:** stack clips on multiple tracks and *Collapse* them into a submaster-like nested effect; step in with the
  Step In button.

## When to nest in animation editorial

- A multi-layer temp comp (background plate, character render, title) that must move as one shot.
- A reusable element: the episode's main titles or a recap montage built once and dropped into every episode.
- Applying one grade/scale to several clips at once.

## When not to

- Before turnover or conform: EDLs cannot describe nests; AAF from Premiere and Resolve can, but many mix and
  online tools flatten or drop them. Un-nest (Premiere: open the nest and copy its clips back; Resolve: *Decompose
  in Place*) before exporting the turnover (see `creative-arts.animation.editorial.editorial-turnover`).
- Audio inside nests is invisible to the AAF audio turnover in some pipelines; keep dialogue un-nested
  (see `creative-arts.animation.editorial.aaf-audio-turnover`).

## Gotchas

- A Premiere nest has its own sequence settings; nesting a 1080 clip in a UHD project then scaling causes soft
  images. Match the nest to the parent.
- Editing inside a nest changes every instance of it; duplicate the nested sequence when one instance must differ.

## Verify

Export the turnover EDL/AAF and re-import it into a blank project: every shot appears as its own event with the
right source and timecode, none as a single nest event.
