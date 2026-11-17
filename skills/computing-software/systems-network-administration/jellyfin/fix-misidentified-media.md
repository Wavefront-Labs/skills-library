---
id: computing-software.systems-network-administration.jellyfin.fix-misidentified-media
name: fix-misidentified-media
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, metadata, misidentified, library-scan, naming, refresh]
level: practitioner
status: docs-checked
description: "Correct wrongly identified shows or movies by moving them out, scanning, renaming to Jellyfin conventions and moving back."
sources: ["https://jellyfin.org/docs/general/administration/troubleshooting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Fixing shows or movies identified incorrectly

If Jellyfin mislabels titles, follow this sequence from the troubleshooting guide:

1. Move one affected show or movie out of the library folder.
2. Start a manual scan: `Dashboard` > `Libraries` > `Libraries` > context menu > `Scan library` > `Refresh`.
3. Rename the files and directories to comply with the official naming documentation for shows or movies.
4. Move the renamed folders back into the target library folder. Follow the expected folder structure and avoid extra subfolders between the library root and your media.
5. Run the manual scan again.

Naming rules differ by media type; see `computing-software.systems-network-administration.jellyfin.movie-library-naming` and `computing-software.systems-network-administration.jellyfin.show-library-naming`. If a title needs a fixed provider match, put the provider id in the name (see `computing-software.systems-network-administration.jellyfin.provider-ids-in-names`).

## Checked

2026-11-03. Confirmed against the Jellyfin Troubleshooting page, Shows Or Movies Not Being Identified Correctly: the five-step move, scan, rename, move back, scan sequence and the menu path. Removed: unsupported explanation and the invented verification.

Method: documentation only; no commands were run.
