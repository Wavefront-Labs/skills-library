---
id: computing-software.systems-network-administration.audiobookshelf.series-management
name: series-management
category: computing-software
field: systems-network-administration
product: audiobookshelf
tags: [series, subseries, sequence, collapse-series, cleanup]
level: practitioner
status: docs-checked
description: "Manage Audiobookshelf series: multiple series per book, decimal sequence ordering, collapsing subseries, and cleaning empty series."
sources:
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/3.series-management.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/1.book-directory-structure.md
  - https://github.com/audiobookshelf/audiobookshelf-docs/blob/master/docs/documentation/libraries/book-library/2.book-metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A book can belong to several series (useful for a universe such as Star Wars or the Foundation universe).

Ordering: by series sequence number, then alphabetically for books with no sequence. Decimals are supported, so a novella can sit between books 2 and 3 as `2.5`. Non-numeric sequence values are allowed but are not sorted in any specific order.

Subseries: every series, including subseries, appears on the library Series page. Books in a series can be collapsed into one entry on the main library page, or when viewing a series to show its subseries.

Empty series: they are removed from the database automatically when no books remain. Some older server versions did not clean up properly. To remove an empty or duplicate series, add any book to it, save the book, then remove the book from the series; that re-triggers cleanup.

Series may also come from tags `series` and `series-part`, folder names, or OPF `calibre:series` fields.

## Checked

2026-11-04. Confirmed against the Audiobookshelf docs: Series Management page, ID3 mapping in the Book Library Structure page and OPF example in the Book Metadata page.

Method: documentation only; no commands were run.
