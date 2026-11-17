---
id: computing-software.systems-network-administration.audiobookshelf.book-folder-structure
name: book-folder-structure
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [library, book-folders, directory-structure, author, series, scanner]
level: practitioner
status: docs-checked
description: "Lay out an Audiobookshelf book library as one folder per book using Author/Series/Book or Author/Book, with supported single-file cases."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Books are defined as a folder. Single-file books may sit in the library root; otherwise every book must be in its own folder. The folder structure is one metadata source, in the form `{Author}/{Series}/{Book}` or `{Author}/{Book}`.

Supported layouts:

```
[Library Root]
  Ender's Game.m4b                       single-file book at root
  Steven Levy/
    Hackers - Heroes of the Computer Revolution {Mike Chamberlain}/
      Audio File.m4a                     author with one book
  1945 - Animal Farm/
    Audiobook.mp3                        book folder in root
  Terry Goodkind/
    Heart of Black Ice - Sister of Darkness/Audio File.m4a
    Sword of Truth/
      Vol 1 - 1994 - Wizards First Rule {Sam Tsoutsouvas}/
        Audio Track 1.mp3
        Audio Track 2.mp3
        Cover.jpg
      Vol 2 - 1995 - Stone of Tears/Audiobook.m4b
```

An author folder can also directly contain an audio file for an "only author book" case. The scanner extracts the first cover image from the file metadata if no image file exists in the book folder.

Ensure the library's metadata priority settings match your file structure.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Book Library Structure page (Directory Structure and File Metadata sections).

Method: documentation only; no commands were run.
