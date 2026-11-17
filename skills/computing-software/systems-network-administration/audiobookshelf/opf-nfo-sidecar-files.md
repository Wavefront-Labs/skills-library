---
id: computing-software.systems-network-administration.audiobookshelf.opf-nfo-sidecar-files
name: opf-nfo-sidecar-files
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [metadata, opf, nfo, calibre, desc-txt, reader-txt]
level: advanced
status: docs-checked
description: "Provide Audiobookshelf metadata through OPF, NFO, desc.txt and reader.txt sidecar files with the supported fields."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**desc.txt / reader.txt:** description from `desc.txt`, narrator from `reader.txt`, in the item folder.

**OPF** (usually from Calibre, which also uses one folder per item). Supported elements include `dc:title`, `dc:description`, `dc:creator` with `opf:role="aut"` (author) or `"nrt"` (narrator), `dc:publisher`, `dc:date`, `dc:language`, `dc:subject` (genres), `dc:identifier` with `opf:scheme="ISBN"` or `"ASIN"`, plus extensions `dc:subtitle`, `dc:tag`, and series via:

```xml
<meta name="calibre:series" content="Example Series" />
<meta name="calibre:series_index" content="1" />
```

**NFO** (used by Plex and Kodi) is a line format:

```
Title: Example Title: Example Subtitle
Author: Example Author
Read by: Example Narrator
Series Name: Example Series
Position in Series: 1
Genre: Fiction, Adventure
Tags: sample
Release Date: 2026-06-19
Publisher: Example Publisher
ISBN: 9781234567897
ASIN: B000000000
Language: eng
```

followed by a `Book Description` block. OPF and NFO fields read: title, author, narrator, publishYear, publisher, isbn, description, genres, language, series, volumeNumber.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Metadata page and Book Library Structure page (Additional Metadata Files).

Method: documentation only; no commands were run.
