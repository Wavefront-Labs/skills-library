---
id: computing-software.systems-network-administration.syncthing.folder-marker-stfolder
name: folder-marker-stfolder
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, folder-marker, stfolder, markername]
level: practitioner
status: docs-checked
description: "Fix Syncthing folder marker missing errors and use markerName on read-only or marker-free folders."
sources: ["https://docs.syncthing.net/users/faq.html", "https://docs.syncthing.net/users/config.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Folder marker (.stfolder)

## Purpose
Syncthing uses a marker, usually `.stfolder`, as a safety check that the folder is properly readable and present on disk. If you remove a USB drive or unmount a filesystem, Syncthing must know whether you really deleted all your files. When the "folder marker missing" error appears, Syncthing assumes the folder has an error and stops syncing it until the marker reappears.

## Resolving the error
- Unmounted storage: mount it again.
- Folder moved: move it back, or remove it in the GUI and re-add at the new path.
- Folder present with all its files but the marker gone: file cleaning software may have removed it, since some remove empty folders and `.stfolder` is often empty (particularly often on Android). Recreate `.stfolder` and add a dummy file in it, or add an exception to the cleaning software.
- If still unsure: remove the folder in the GUI and re-add it at the same location. Syncthing attempts to recreate `.stfolder` automatically and resets the database state of the folder, so it is considered new and its files are merged with files from remote devices.

Once syncing resumes, all changes made to the folder locally are synced, and missing files are considered deletions, so be certain the folder is complete.

## Custom marker
`markerName` is the name of a directory or file in the folder root used as the marker. Syncthing only creates a marker directory for the default `.stfolder`, not otherwise.

```xml
<folder id="media" path="/path/to/media">
  <markerName>.keep</markerName>
</folder>
```

## Checked
2026-11-04. Read the FAQ entry on the folder marker error and the `markerName` entry in the config page: marker purpose, stop-until-reappears behaviour, remount/move/cleaner/re-add remedies, deletions on resume, and the marker-directory creation rule. Removed the claim that a custom marker suits read-only media, which the pages do not state, and the "last resort" label.
Method: documentation only; no commands were run.
