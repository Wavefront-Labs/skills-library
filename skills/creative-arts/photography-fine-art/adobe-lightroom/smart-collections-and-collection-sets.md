---
id: creative-arts.photography-fine-art.adobe-lightroom.smart-collections-and-collection-sets
name: smart-collections-and-collection-sets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, smart-collections, lightroom-library, collection-sets, collections, target-collection, lightroom-classic]
level: practitioner
status: draft
description: "Organise projects in Lightroom Classic with collection sets, collections and rule-based smart collections for work-in-progress, print queues and QA."
sources: ["https://helpx.adobe.com/lightroom-classic/help/photo-collections.html", "https://helpx.adobe.com/lightroom-classic/desktop/organize-photos-in-lightroom-classic/smart-collections-criteria-in-lightroom-classic.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart collections and collection sets

Folders are where files live; collections are how you think. Never reorganise folders to build a project.

## Structure
- **Collection set** per body of work: `Projects > Coastline (2024-)`. Inside it: `01 Selects`, `02 Sequence`, `03 Print queue`, `Exhibited 2026`.
- Regular collections allow a custom sort order (drag in Grid): the basis for sequencing.
- Mark one collection as **Target** (right-click > Set as Target Collection) and press `B` to add photos to it.
- Virtual copies can live in collections, so colour and B&W versions can be sequenced separately.

## Smart collections (rule-based, update live)
Create with `+` > Create Smart Collection. Match all/any; Alt/Option-click `+` for nested rule groups. Useful ones:
- **Needs keywords**: Keywords are empty AND Folder contains `2026`.
- **Unedited picks**: Pick Flag is flagged AND Develop > Has Edits is false.
- **Missing copyright**: Copyright is empty.
- **Print candidates**: Rating >= 4 AND Collection contains `Selects` AND Cropped is true.
- **AI edits audit**: Develop > Has AI is true (Denoise, Super Resolution, AI masks, Generative Remove), useful for disclosure rules in competitions.
- **Recent**: Capture Date is in the last 30 days.

## Share and reuse
- Right-click a smart collection > Export Smart Collection Settings (`.lrsmcol`) and import into another catalog.
- Defaults (Colored Red, Five Stars, Past Month, Recently Modified, Without Keywords) can be edited or deleted.

## Gotchas
- Smart collections cannot be manually sorted or have photos dragged in.
- Rules on "Collection contains" match by name text: name collections consistently.

## Verify
- [ ] The "Missing copyright" smart collection shows 0 photos before any export batch.
