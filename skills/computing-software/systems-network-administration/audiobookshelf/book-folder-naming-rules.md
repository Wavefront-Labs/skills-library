---
id: computing-software.systems-network-administration.audiobookshelf.book-folder-naming-rules
name: book-folder-naming-rules
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [library, folder-naming, series-sequence, publish-year, narrator, asin, disc]
level: practitioner
status: docs-checked
description: "Embed series sequence, year, narrator, subtitle, disc and ASIN in Audiobookshelf book folder names using the supported patterns."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Book folder names can carry metadata:

- **Series sequence** - case insensitive, decimals allowed. Anywhere in the name. It must be followed by ` - ` or by `. `, e.g. `1 - Title`, `1. Title`. If not at the start, it must be preceded by ` - ` plus `Vol`, `Vol.`, `Volume` or `Book`.
- **Publish year** - first part of the name, or directly after a series sequence, separated by ` - `: `1994 - Title`.
- **Narrator** - in curly braces: `{Sam Tsoutsouvas}`.
- **Disc** - subfolders named `Disc`, `CD` or `Disk` plus a number, case insensitive (`Disc 1`, `CD 2`, `Disk 3`, `Disc 004`, `Disc1`).
- **Subtitle** - requires subtitle parsing enabled in settings; separated by ` - `.
- **ASIN** - Audible serial in brackets, `1. Wizards First Rule [B002V0QK4C]`. The Audible ASIN differs from the Amazon ASIN.

Examples: `Vol. 1 - 1994 - Wizards First Rule - A Really Good Subtitle {Sam Tsoutsouvas}` and `(1994) - Wizards First Rule - A Really Good Subtitle`.

Metadata priority applies: folder structure is lowest by default.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (Book Folder Naming) and Book Metadata page (priority).

Method: documentation only; no commands were run.
