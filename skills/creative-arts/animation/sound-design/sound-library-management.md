---
id: creative-arts.animation.sound-design.sound-library-management
name: sound-library-management
category: creative-arts
field: animation
product: sound-design
tags: [sound-library, sfx-library, ucs, universal-category-system, soundminer, metadata, bwf, ixml, licensing, search]
level: practitioner
status: draft
description: "Organise an SFX library so effects are found by search in seconds: UCS categories and file naming, embedded BWF/iXML metadata, search tools and licence tracking."
sources:
  - https://universalcategorysystem.com/
  - https://store.soundminer.com/
  - https://tech.ebu.ch/publications/tech3285
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sound library management and metadata search

**Goal:** any editor can find "metal door slam, heavy, reverberant" in seconds, know its licence, and get the
same results on every workstation.

## Naming: Universal Category System (UCS)

UCS is a public, free standard of categories/subcategories with CatIDs and a file naming scheme:

`CatID_FXName_CreatorID_SourceID.wav`, e.g. `DOORMetl_Heavy Slam Reverb_JDS_MYLIB.wav`

- CatID = category+subcategory short code (DOORMetl = Doors / Metal). The UCS spreadsheet lists them all, with
  synonyms, in several languages.
- FXName = short human description; CreatorID = recordist/designer; SourceID = library/project.

## Metadata

Embed descriptions in the file so they travel with it:

- **BWF bext** chunk: Description, Originator, date (see `creative-arts.animation.sound-design.bwf-ixml-metadata`).
- **iXML** and Soundminer's metadata fields: keywords, category, microphone, licence.
- Search apps (Soundminer, Soundly, BaseHead, Reaper's Media Explorer with database) index these fields.

## Tools

| Tool | Notes |
|---|---|
| Soundminer | industry standard, embeds metadata, transfers to DAW with pitch/selection |
| Soundly | cloud + local, team libraries, licensing per seat |
| BaseHead | fast local search |
| Reaper Media Explorer | free with Reaper; databases search file names and metadata |

## Licence tracking

Every file must have a licence field: purchased library (licence terms), CC0, CC-BY (attribution required in
credits), or original recording. CC-BY and other non-CC0 assets need logging in the episode's asset ledger for
credits (see `creative-arts.animation.pipeline.asset-sourcing`).

## Verify

Search three terms ("whoosh metal", "crowd walla interior", "cartoon boing") on two machines: same results, each
file shows description and licence, and every file name follows UCS.
