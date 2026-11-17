---
id: creative-arts.photography-fine-art.adobe-lightroom.import-dialog-and-import-presets
name: import-dialog-and-import-presets
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, lightroom-import, lightroom-catalog, import-presets, file-renaming, copy-vs-add, lightroom-classic]
level: practitioner
status: draft
description: "Import into Lightroom Classic with Copy, Move or Add, file renaming, a second backup copy, metadata and develop presets, saved as an import preset."
sources: ["https://helpx.adobe.com/lightroom-classic/help/photo-video-import-options.html", "https://helpx.adobe.com/lightroom-classic/help/lightroom-catalog-basics.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Import photos)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Import dialog and import presets

## Choose the operation (top centre of the Import window)
- **Copy as DNG / Copy**: copies from the card to your archive drive and leaves the card untouched. Use for card imports.
- **Move**: moves files already on a disk into a new folder structure (removes them from the source).
- **Add**: catalogues files where they already are. Use for files already on the archive drive.
- Copy as DNG converts raw to DNG on the way in; keep the original raw if you may want the camera maker's software later.

## Right-hand panels, top to bottom
1. **File Handling**: Build Previews (Minimal for speed, Standard if you will browse in Library, 1:1 if you will zoom-cull immediately); Build Smart Previews if you will edit away from the drive; Don't Import Suspected Duplicates on; **Make a Second Copy To** a second drive (a one-time backup of originals, not a backup strategy); Add to Collection.
2. **File Renaming**: a template such as `YYYYMMDD_shoot_0001` (Edit > custom text + date + sequence). Rename at import, never later in Explorer/Finder.
3. **Apply During Import**: Develop Settings (a neutral starting preset, e.g. lens corrections on), Metadata (your copyright IPTC preset), Keywords (broad shoot keywords).
4. **Destination**: archive root, Organize = By Date with a format like `2026/2026-10-16`, or Into One Folder with a named subfolder per shoot.

## Save it
Bottom of the dialog: Import Preset > Save Current Settings as New Preset ("Card to archive", "Add in place"). Collapse to the compact dialog for one-click repeat imports.

## Gotchas
- A Move or Add import from a card leaves files on removable media: they go offline when the card is ejected.
- Suspected duplicates are matched on original filename, capture time and file size; renamed copies can slip through.
- Turning off "Show import dialog when a memory card is detected" (Preferences > General) avoids accidental imports.

## Verify
- [ ] Files appear in the expected dated folder in the Folders panel and on disk.
- [ ] Copyright metadata present in the Metadata panel; second copy exists on the backup drive.
