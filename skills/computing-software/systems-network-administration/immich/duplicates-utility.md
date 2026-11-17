---
id: computing-software.systems-network-administration.immich.duplicates-utility
name: duplicates-utility
category: computing-software
field: systems-network-administration
product: immich
tags: [duplicates, deduplicate, clip, review, metadata-sync]
level: practitioner
status: docs-checked
description: "Review visually similar assets in Immich's duplicates utility, how keepers are preselected, and which metadata is merged into the kept asset."
sources:
  - https://docs.immich.app/features/duplicates-utility
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: resolve near-duplicate photos without losing metadata.

Duplicate detection uses machine learning and is enabled by default. For when the job runs, the page points to Jobs and Workers. Once an asset joins a duplicate group, it appears in the "Review duplicates" utility.

On the review page you choose which assets to keep and which to trash. If you keep more than one, you can have Immich stack the kept assets automatically.

Automatic preselection ("Deduplicate All" or suggestions) prefers:

1. Larger file size in bytes.
2. More EXIF data.

Metadata from trashed assets is merged into the kept one only when exactly one asset is kept and at least one is trashed. When several are kept, metadata is not merged.

What synchronises:

- Album: the kept asset joins every album the others were in.
- Favorite: favorited if any asset in the group was.
- Rating: the highest rating wins.
- Description: all descriptions are combined.
- Visibility: the most restrictive applies.
- Location: latitude and longitude copied if every asset that has geolocation shares the same coordinates.
- Tags: merged from all assets.

Partner sharing can show duplicates on your timeline, because detection runs per user only (stated on the Partner Sharing page).

## Checked

2026-11-09. Confirmed against the Duplicates Utility page: ML-based and on by default, Review duplicates, stacking option, preselection by byte size then EXIF count, metadata sync rules and the table. Removed: the claims that detection runs after Smart Search and depends on its output, which the page does not state.
Method: documentation only; no commands were run.
