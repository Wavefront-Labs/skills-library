---
id: creative-arts.photography-fine-art.adobe-lightroom.folders-panel-missing-files-and-relinking
name: folders-panel-missing-files-and-relinking
category: creative-arts
field: photography-fine-art
product: adobe-lightroom
tags: [adobe-lightroom, missing-files-relink, lightroom-catalog, folders-panel, synchronize-folder, find-missing-folder, lightroom-classic]
level: practitioner
status: draft
description: "Fix missing photos and folders in Lightroom Classic: Find Missing Folder, Locate, Update Folder Location, Synchronize Folder, and moving files inside Lightroom."
sources: ["https://helpx.adobe.com/lightroom-classic/help/lightroom-catalog-basics.html", "https://helpx.adobe.com/lightroom-classic/kb/lightroom-basic-troubleshooting-fix-most-issues.html", "https://helpx.adobe.com/lightroom-classic/user-guide.html (Locate missing photos)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Folders panel, missing files and relinking

Lightroom stores the absolute path to each file. If a file or folder is moved, renamed or the drive letter changes outside Lightroom, the folder shows a **question mark** and thumbnails show an **exclamation badge**.

## Relink a whole folder (fastest)
- Right-click the greyed folder > **Find Missing Folder...** and pick its new location. All photos inside relink at once.
- For a drive-letter change, relink the **top-level** folder: right-click > Show Parent Folder until you reach the root, then Find Missing Folder there.
- **Update Folder Location** does the same for a folder that is online but you want pointed elsewhere (e.g. after copying the archive to a new drive).

## Relink single files
- Click the exclamation badge > **Locate**. Keep "Find nearby missing photos" ticked to relink siblings in the same folder.
- Library > Find All Missing Photos builds a temporary collection of every missing file.

## Bring in files added outside Lightroom
- Right-click folder > **Synchronize Folder...**: imports new files, removes catalog entries for deleted files and can scan for metadata updates. Untick "Show import dialog" to add silently.

## Prevent it
- Move, rename and delete inside Lightroom only (drag in the Folders panel; Library > Rename Photo).
- Give archive drives a fixed drive letter (Windows Disk Management) or a unique volume name (macOS).
- Right-click a folder > Add Parent Folder to see the full tree so moves happen at the right level.
- Use one archive root so the whole library relinks in one step.

## Verify
- [ ] Library > Find All Missing Photos returns an empty collection.
