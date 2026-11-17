---
id: computing-software.systems-network-administration.audiobookshelf.match-and-quick-match
name: match-and-quick-match
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [metadata, match, quick-match, providers, scan, api]
level: practitioner
status: docs-checked
description: "Differentiate scanning from matching in Audiobookshelf and use Match versus Quick Match against online metadata providers."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/faq/server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A scan reads **local** files (folders, tags, sidecars). A match uses what the scan found to look the book up at an online provider. Matching never happens automatically during a scan; it must be started by a user or through the API. Scans themselves run via the File Watcher or Periodic Scans in library settings.

**Match** (book details page): choose the search result and pick individual fields to take, preserving local metadata. You can set a default provider per library or choose another when searching.

**Quick Match:** automatically picks the closest result, based on provider result priority and how close your file's duration is to the provider's duration. It is not always accurate when the book is missing from the provider; try a manual match or another provider.

Quick-match a whole library with "Match Books" in the library dropdown in server settings, or select several books in the library view. Choose whether provider cover and metadata overwrite what the database holds.

## Checked

Method: docs-checked 2026-11-09 against the Book Metadata page and the FAQ server page of the Audiobookshelf docs repo (full raw markdown read).
