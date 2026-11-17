---
id: creative-arts.graphic-design.adobe-photoshop.artboards-for-multi-size-screen-work
name: artboards-for-multi-size-screen-work
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, photoshop-document-setup, photoshop-artboards, artboard-tool, multi-size, social-sizes, banner-sets, export-artboards, linked-smart-objects]
level: practitioner
status: draft
description: "Build a set of sizes (social formats, banners, screens) in one PSD with artboards, share assets via smart objects, and export each artboard."
sources:
  - https://helpx.adobe.com/photoshop/using/artboards.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Artboards for multi-size screen work

**Goal:** all sizes of a campaign or screen set in one PSD, sharing assets so one edit updates every size.

## Create
- File > New > tick **Artboards**, or in an existing file select layers > Layer > New > Artboard
  from Layers. **Artboard tool** (nested under Move, V): drag to draw; click the + icons beside
  an artboard to add one next to it; Alt/Option+drag to duplicate with contents.
- Set size from presets in the Options bar (iPhone, Web, social) or type W/H in Properties.
- Name artboards by deliverable: `feed-4x5`, `story-9x16`, `leaderboard-728x90`.

## Structure
- Each artboard is a top-level group in the Layers panel; layers inside clip to it.
- Background colour per artboard in Properties (White, Black, Transparent, Other).
- Layers outside artboards sit on the canvas and do not export.

## Share assets between sizes
- Convert the shared elements (logo, product cut-out, headline lockup) to **smart objects**,
  then duplicate the smart object instance into each artboard (Layer > New Smart Object via
  Copy makes an independent copy; plain duplicate keeps it linked to the same contents).
  Editing the contents of one updates all instances; each instance can be scaled differently.
- For assets shared across files, use **linked smart objects** (File > Place Linked) or CC
  Libraries items.

## Export
- File > Export > **Artboards to Files** (format, prefix, include overlapping areas or not).
- File > Export > **Export As** with artboards selected: per-artboard formats and @2x scales.
- Artboards to PDF for a review deck.

## Gotchas
- Effects or layers overlapping into a neighbouring artboard are clipped - keep spacing between artboards.
- Artboards cannot be nested or rotated; very large files with many artboards slow down -
  use linked smart objects to keep the PSD small.
- Moving a layer across artboard bounds re-parents it into the other artboard.

## Verify
- [ ] Every required size exists as a named artboard.
- [ ] Editing a shared smart object updates it in every artboard.
- [ ] Export produces one correctly named file per artboard.
