---
id: computing-software.systems-network-administration.immich.supported-formats
name: supported-formats
category: computing-software
field: systems-network-administration
product: immich
tags: [heic, raw, formats, video, mime-types]
level: intro
status: docs-checked
description: "Which image and video formats and extensions Immich accepts, and where the authoritative list lives in the source."
sources:
  - https://docs.immich.app/features/supported-formats
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: check whether a file will be accepted before you import or upload it.

The docs list the most common formats. For the full list, the docs refer to the Immich source code.

Images (all supported):

- AVIF `.avif`, BMP `.bmp`, GIF `.gif`.
- HEIC `.heic` and HEIF `.heif`.
- JPEG 2000 `.jp2`; JPEG `.jfif` `.jpeg` `.jpg` `.jpe` `.insp`; JPEG XL `.jxl`.
- MPO `.mpo` (multi-picture).
- PNG `.png`, PSD `.psd` (Adobe Photoshop), SVG `.svg`.
- RAW `.raw` and RW2 `.rw2`.
- TIFF `.tif` `.tiff`, WEBP `.webp`.

Videos (all supported):

- 3GPP `.3gp` `.3gpp`, AVI `.avi`, FLV `.flv`, M4V `.m4v`.
- Matroska `.mkv`, MP2T `.mts` `.m2ts` `.m2t` `.ts`.
- MP4 `.mp4` `.insv`, MPEG `.mpg` `.mpe` `.mpeg`, MXF `.mxf`.
- QuickTime `.mov`, WEBM `.webm`, WMV `.wmv`.

If a file type is missing from the tables, check the Immich source code before concluding it is unsupported.

## Checked

2026-11-09: read https://docs.immich.app/features/supported-formats in full; every extension and note above matches the image and video tables. Removed the mime-types file path, the exclusion-pattern example, the transcode setting name and the `IMMICH_PROCESS_INVALID_IMAGES` line (not on the page) and dropped the three related sources.

Method: documentation only; no commands were run.
