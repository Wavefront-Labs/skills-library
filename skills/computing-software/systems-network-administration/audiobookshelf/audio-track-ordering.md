---
id: computing-software.systems-network-administration.audiobookshelf.audio-track-ordering
name: audio-track-ordering
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [tracks, disc-number, track-number, manage-tracks, multi-file]
level: practitioner
status: docs-checked
description: "Order multi-file audiobook tracks by disc then track number from tags or filenames, and fix order with Manage Tracks."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each audio file is a track with a track number parsed from the filename and from ID3 tags. Multi-disc books order first by disc, then by track.

| Key | ID3 tags | Filename |
| --- | --- | --- |
| DiscNumber | discnumber, disc, disk, tpos | number after "Disc" or "CD", e.g. `Atlas Shrugged CD 01 - 1.mp3` |
| TrackNumber | track, trck, trk | first number after removing title, publish year, series, author, disc number |

The scanner picks the more accurate value between filename and tag.

If order is wrong, open the audiobook details page and use **Manage Tracks** to reorder tracks manually and enable or disable individual tracks.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (Audiobook Tracks).

Method: documentation only; no commands were run.
