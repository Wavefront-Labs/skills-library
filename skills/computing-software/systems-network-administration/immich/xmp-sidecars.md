---
id: computing-software.systems-network-administration.immich.xmp-sidecars
name: xmp-sidecars
category: computing-software
field: systems-network-administration
product: immich
tags: [xmp, sidecar, metadata, discover, sync, digikam]
level: practitioner
status: docs-checked
description: "How Immich reads and writes XMP sidecar files: supported fields, file naming, CLI and external library behaviour, DISCOVER and SYNC jobs, read-only mount trap."
sources:
  - https://docs.immich.app/features/xmp-sidecars
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: keep metadata edited in tools such as Lightroom, Darktable or digiKam in sync with Immich.

Immich reads `.xmp` files during metadata extraction and writes them in the Sidecar Write job. Writes merge with existing fields rather than replacing the file. After you edit a description, rating or tags, a Sidecar Write job is queued automatically.

Fields written to XMP:

- Description: `dc:description`, `tiff:ImageDescription`.
- Rating: `xmp:Rating`.
- DateTime: `exif:DateTimeOriginal`, `photoshop:DateCreated`.
- Location: `exif:GPSLatitude`, `exif:GPSLongitude`.
- Tags: `digiKam:TagsList`.

Tags are read in priority order `digiKam:TagsList`, `lr:HierarchicalSubject`, `IPTC:Keywords`. Other fields stay in the file and are not searchable in Immich.

Naming: the sidecar shares the media base name. `IMG_0001.jpg.xmp` is preferred, `IMG_0001.xmp` is the fallback, `myphoto_meta.xmp` is not recognised. If both exist, `.jpg.xmp` wins.

Uploads (CLI): the sidecar placed next to the media is detected and copied with the file into the library, renamed to match, for example `IMG_0001.jpg.xmp`. Later UI edits update both the database and the copy.

External libraries: the `DISCOVER` job links `.xmp` files next to existing media without moving anything. `SYNC` re-reads existing sidecars after external edits. Write-back needs write access to the mount.

Danger: on a read-only mount, Immich cannot update either the sidecar or the database, and metadata edits silently fail with no warning. Mount with write access if you want edits.

## Checked

2026-11-09. Confirmed against the XMP Sidecars page: read and write jobs, merge on write, automatic Sidecar Write job, field table, tag read priority, naming rules, CLI and external library behaviour, DISCOVER and SYNC jobs, read-only warning. The page also lists a prioritized DateTime read order, not reproduced here.
Method: documentation only; no commands were run.
