---
id: creative-arts.photography-fine-art.adobe-lightroom.smart-previews-and-offline-editing
name: smart-previews-and-offline-editing
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, smart-previews, lightroom-catalog, offline-editing, lrdata, lightroom-classic]
level: practitioner
status: draft
description: "Build Lightroom Classic smart previews to edit with the originals drive disconnected, sync changes on reconnect and know which tasks still need originals."
sources: ["https://helpx.adobe.com/lightroom-classic/help/lightroom-smart-previews.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Smart Previews)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Smart previews and offline editing

A smart preview is a lossy DNG at 2560 px on the long edge, stored in `<catalog name> Smart Previews.lrdata` next to the catalog. Develop edits made on it apply to the original when the drive returns.

## Build them
- At import: File Handling > **Build Smart Previews**.
- Later: select photos > Library > Previews > **Build Smart Previews**, or click "Original" under the Histogram and choose Build Smart Previews.
- Status under the Histogram: *Original*, *Original + Smart Preview*, *Smart Preview* (original offline), or *Photo is missing*.

## Working offline
1. Before travel, build smart previews for the collections you plan to edit.
2. Eject the image drive; edit, keyword, flag and crop as normal.
3. Reconnect: changes are already in the catalog and apply to originals with no action needed.
- Preferences > Performance > **Use Smart Previews instead of Originals for image editing** makes Develop faster on slow drives or big files even when originals are online (final output still uses originals).

## What needs the originals
- Export at full size (exports from smart previews are limited to 2560 px), printing at full resolution, Edit in Photoshop, Photo Merge, Enhance (Denoise/Super Resolution) and 1:1 accurate sharpening judgement.

## Housekeeping
- Discard when done: Library > Previews > Discard Smart Previews. They take roughly 1 MB each.
- The `.lrdata` folder is not part of the catalog backup.

## Verify
- [ ] With the drive ejected, Histogram status reads "Smart Preview" and Develop sliders are active.
