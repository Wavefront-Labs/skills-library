---
id: computing-software.systems-network-administration.audiobookshelf.book-grouping-problem-fix
name: book-grouping-problem-fix
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [library, grouping, inode, file-watcher, rescan, troubleshooting]
level: practitioner
status: docs-checked
description: "Fix multiple books showing as one Audiobookshelf book by correcting the folder layout, removing the item and rescanning."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Symptom: several books appear as a single book. The docs call this almost always a violation of the one-folder-per-book rule. Example of a wrong layout that groups everything as one `Sword of Truth Vol 2` book: an audio file `Sword of Truth Vol 2.mp3` placed directly in the author folder next to the book subfolders.

Why fixing the folders is not enough: Audiobookshelf tracks file moves by file **inode**, so once files are grouped under one book the grouping persists after you reorganise.

Fix:

1. Correct the directory structure.
2. Remove the grouped book from the Audiobookshelf database using the interface (this removes progress for those books when they are re-added).
3. Rescan the library.

Another cause: other tools moving files around your library with "watch for file changes" enabled. The server may scan mid-move and merge files. Temporarily moving a book to an unsupported location during reorganisation can do the same.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (Book Grouping) and FAQ server page (multiple books as one).

Method: documentation only; no commands were run.
