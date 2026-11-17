---
id: computing-software.systems-network-administration.audiobookshelf.audio-id3-tag-mapping
name: audio-id3-tag-mapping
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [metadata, id3, tags, ffprobe, composer, narrator, series]
level: advanced
status: docs-checked
description: "Map ID3 and audio tags to Audiobookshelf fields: artist, album, composer as narrator, series, series-part, asin and chapters."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Audiobookshelf reads tags case-insensitively; the second tag after "/" is a fallback.

| Tag | Field |
| --- | --- |
| artist / album-artist | Author |
| album / title | Title |
| subtitle | Subtitle |
| publisher | Publisher |
| year | Publish Year |
| composer | Narrator |
| description | Description |
| genre | Genres |
| series / mvnm | Series |
| series-part / mvin | Series Sequence |
| language / lang | Language |
| isbn | ISBN |
| asin / audible_asin | ASIN |
| Overdrive MediaMarkers | Chapters |

Genre can hold several values split by `/`, `//` or `;`, for example `Science Fiction/Fiction/Fantasy`. Chapter extraction from Overdrive MediaMarkers must be enabled in server settings.

The metadata from the **first audio track** (after sorting by disc and track) is used. If no audio file exists, e-book file metadata is used. The first cover image in the file metadata is used only when no image file exists in the folder.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (File Metadata) and Book Metadata page (File Metadata).

Method: documentation only; no commands were run.
