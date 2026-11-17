---
id: creative-arts.photography-fine-art.adobe-lightroom.catalog-backup-and-restore
name: catalog-backup-and-restore
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, catalog-backup, lightroom-catalog, catalog-restore, lrcat, optimize-catalog, lightroom-classic]
level: practitioner
status: draft
description: "Schedule Lightroom Classic catalog backups, test them, prune old backup zips and restore a damaged catalog, keeping image backups separate."
sources: ["https://helpx.adobe.com/lightroom-classic/help/back-catalog.html", "https://helpx.adobe.com/lightroom-classic/help/create-catalogs.html", "https://helpx.adobe.com/lightroom-classic/kb/lightroom-basic-troubleshooting-fix-most-issues.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Catalog backup and restore

The `.lrcat` file holds every edit, keyword, collection and flag. Lightroom's catalog backup covers **only the catalog**, never the image files or exports.

## Schedule
1. Edit/Lightroom Classic > Catalog Settings > General > Back up catalog: **Once a day, when exiting** (or Once a week for light use). "When Lightroom next exits" runs once then reverts to Never.
2. On exit, the backup dialog lets you set the folder: choose a different physical drive from the catalog (by default it sits in `Backups` next to the catalog).
3. Leave **Test integrity before backing up** and **Optimize catalog after backing up** ticked.

## Housekeeping
- Each backup is a dated folder holding a zipped catalog. They are never deleted automatically: keep the last ~10 and delete older ones.
- Previews (`.lrdata`) are not backed up and do not need to be: they rebuild.
- Your image drive needs its own backup (see the 3-2-1 archive backup skill). Also back up presets and templates (Preferences > Presets > Show Lightroom Develop Presets).
- The backup is in the dated folder only after exit completes; force-quitting skips it.

## Restore
1. Quit Lightroom. Rename the damaged `.lrcat` (do not delete it).
2. Unzip the latest backup zip; move the `.lrcat` into the original catalog folder.
3. Double-click it (or File > Open Catalog). Edits made since that backup are lost unless "Automatically write changes into XMP" was on, in which case select all and Metadata > Read Metadata from Files for raw files whose XMP is newer (Lightroom marks them with the metadata-conflict badge).
4. If Lightroom reports the catalog as corrupt on launch, let it try repair once; if repair fails, restore.

## Gotchas
- Catalogs must be on a local drive; network drives are unsupported and backup to network locations has known failures.
- A `.lrcat-lock` file left after a crash blocks opening: delete it only when Lightroom is fully closed.

## Verify
- [ ] Open a backup copy as a test catalog once a quarter; photos appear and edits are intact.
