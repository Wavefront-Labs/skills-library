---
id: computing-software.systems-network-administration.audiobookshelf.author-folder-naming
name: author-folder-naming
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [library, author-names, folder-naming, scanner, metadata]
level: practitioner
status: docs-checked
description: "Name author folders so Audiobookshelf extracts one or several authors correctly, using First Last, Last First, and the separators."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/common-content/1.overview.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authors can be written `First Last` or `Last, First`. Multiple authors are separated by `,`, `;`, `&` or `and`.

Supported examples:

```
Ichiro Kishimi
Kishimi, Ichiro
Ichiro Kishimi, Fumitake Koga
Kishimi, Ichiro, Koga, Fumitake
Ichiro Kishimi & Fumitake Koga
Kishimi, Ichiro & Koga, Fumitake
Terry Goodkind, Ichiro Kishimi and Fumitake Koga
```

Gotcha: author names are not punctuation or whitespace aware. `J.R.R. Tolkein` and `J. R. R. Tolkein` become **separate authors**.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (Author Folder Naming).

Method: documentation only; no commands were run.
