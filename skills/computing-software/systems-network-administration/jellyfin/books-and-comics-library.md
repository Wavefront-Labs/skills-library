---
id: computing-software.systems-network-administration.jellyfin.books-and-comics-library
name: books-and-comics-library
category: computing-software
field: systems-network-administration
product: jellyfin
tags: [jellyfin, books, audiobooks, comics, epub, comicinfo-xml, content-opf, openlibrary]
level: practitioner
status: docs-checked
description: "Structure a Jellyfin Books library by type, supply metadata via OPF or ComicInfo.xml, and know the supported formats."
sources: ["https://jellyfin.org/docs/general/server/media/books/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Books, audiobooks and comics

Organise by type (Audiobooks, Books, Comics), then optionally by author. Each book goes in its own folder.

```txt
Books
├── Audiobooks
│   └── Book3
│       ├── Book3.aac
│       ├── content.opf
│       └── cover.jpg
├── Books
│   └── Author
│       └── Book6
│           ├── Book6.epub
│           └── metadata.opf
└── Comics
    └── Comic (2008)
        ├── ComicInfo.xml
        └── Comic #001 (2008).cbr
```

**Formats.** Audiobooks accept most common audio extensions. Other books: azw, azw3, cb7, cbr, cbt, cbz, epub, mobi, pdf, zip, rar, 7z. Read-along audiobooks are not supported.

**Metadata.** Online providers include GoogleBooks, ComicVine and OpenLibrary, plus embedded metadata. Audio books read embedded tags. Epub can embed metadata; other formats use an external `content.opf`, `metadata.opf` or `ComicInfo.xml` (ComicRack and ComicBookLover formats are supported). Year and issue number can be put in the file name; for multi-year comics or magazines use the first issue's year.

**Images.** Embedded in those files, or named: Primary `folder`, `poster`, `cover`; Banner `banner`; Logo `logo`; Thumb `thumb`, `landscape`.

FLAC audiobooks with WebP images or ID3 tags may need `Always remux FLAC audio files` in client settings.

## Checked

2026-11-08. Confirmed against the Jellyfin Books page: folder layout by type, supported formats, read-along audiobooks unsupported, metadata providers, opf and ComicInfo.xml files, year in comic file names, image names table, FLAC remux hint. Page read in full.

Method: documentation only; no commands were run.
