---
id: creative-arts.photography-fine-art.adobe-lightroom.keyword-hierarchy-and-keyword-sets
name: keyword-hierarchy-and-keyword-sets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, keyword-hierarchy, lightroom-library, keyword-sets, keyword-list, controlled-vocabulary, lightroom-classic]
level: practitioner
status: draft
description: "Build a Lightroom Classic keyword hierarchy with synonyms and export rules, use keyword sets and the painter, and import or export keyword lists."
sources: ["https://helpx.adobe.com/lightroom-classic/desktop/help/library-module-basic-workflow.html", "https://helpx.adobe.com/lightroom-classic/help/finding-photos-catalog.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Keywords)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keyword hierarchy and keyword sets

## Design the hierarchy
- Top-level parents by facet: `Places`, `Subjects`, `Projects`, `Techniques`, `People`, `_Admin`.
- Nest child > parent: `Places > Europe > Scotland > Isle of Skye`. Assigning a child implies its parents.
- Use singular nouns and one spelling; add alternative spellings as **Synonyms** (Keyword List > right-click > Edit Keyword Tag).
- For structural or private keywords (`_Admin`, `To print`), untick **Include on Export** so they never leak into exported files. Tick **Export Containing Keywords** where parents should go out too.

## Build it
- Keyword List panel: `+` to create; drag keywords onto others to nest.
- Typing `Isle of Skye < Scotland` (child < parent) in the Keywording panel creates and nests both keywords in one go.
- Metadata > Import Keywords reads a tab-indented text file; Export Keywords writes one, useful to share a vocabulary across catalogs.

## Apply fast
- **Keyword sets** (Keywording panel > Keyword Set > Edit Set): nine keywords per set, applied with Alt/Option+1-9. Make a set per project or location trip.
- **Painter** tool (spray can, Library toolbar): set to Keywords, then click thumbnails.
- Keyword suggestions update based on co-occurring keywords.

## Maintain
- Merge duplicates by hand: click the count arrow beside the wrong keyword to show its photos, assign the correct keyword to them, then delete the wrong one (dragging only nests, it does not merge).
- Metadata > Purge Unused Keywords removes zero-count keywords.

## Verify
- [ ] Export a test JPEG and read its keywords in Bridge/exiftool: no `_Admin` terms present.
