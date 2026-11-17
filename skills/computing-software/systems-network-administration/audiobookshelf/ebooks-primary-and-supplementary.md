---
id: computing-software.systems-network-administration.audiobookshelf.ebooks-primary-and-supplementary
name: ebooks-primary-and-supplementary
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [ebooks, epub, pdf, cbz, primary-ebook, supplementary]
level: practitioner
status: docs-checked
description: "Handle e-books in Audiobookshelf: supported extensions, primary versus supplementary files, and the Audiobooks only setting."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/4.ebooks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supported extensions: `epub`, `pdf`, `cbr`, `cbz`, `azw3`, `mobi`. Progress is not tracked for `azw3` and `mobi`. An item can hold both audio and e-book files in the same folder. Audiobookshelf has only basic readers; Calibre-Web, Kavita or Komga give more.

Each item has at most one **Primary** e-book and any number of **Supplementary** ones. Progress is stored only for the Primary. If several e-books are found during a scan, `epub` has priority as primary. The primary is marked with a green check in the file list. The blue Read button resumes the primary from stored progress (audio and e-book progress are separate); the Read icon in the file table opens a file from the start. Change primary/supplementary with the dropdown in the file table.

The **Audiobooks only** library setting sets all e-book files as supplementary. Without it, the scanner treats e-book files like audio files when deciding if a folder is a library item.

## Checked

Method: docs-checked 2026-11-09 against the E-books page of the Audiobookshelf docs repo, read in full from raw markdown.
