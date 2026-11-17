---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.sqlite-database-forensics
name: sqlite-database-forensics
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [sqlite-forensics, wal, freelist, deleted-records, browser-forensics, mobile-forensics, dfir]
level: advanced
status: docs-checked
description: "Examine SQLite databases forensically: acquiring with WAL and journal files, where deleted data can remain (WAL frames, freelist, freeblocks, journal), and a record parser."
sources: ["https://www.sqlite.org/fileformat2.html", "https://www.sqlite.org/wal.html", "https://github.com/mdegrazia/SQLite-Deleted-Records-Parser"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLite database forensics

**Goal:** extract both live and deleted data from SQLite databases (browsers, mobile apps,
messaging apps) without destroying the deleted remnants.

## Acquire properly
- Copy the database **together with** its `-wal` file (write-ahead log) and `-shm` file
  (wal-index shared memory), and any rollback journal file if present. In WAL mode, committed
  changes live in the WAL until a checkpoint moves them into the main file.
- Do not open the original with a normal client. By default SQLite checkpoints the WAL
  automatically when a COMMIT leaves the WAL at 1000 pages or more, and when the last
  connection to the database closes. A checkpoint transfers WAL content into the database file.
- Opening a WAL-mode database needs write access to the `-shm`/`-wal` files or their
  directory, unless they already exist and are readable or the connection uses the `immutable`
  query parameter. Work on copies so none of this touches the evidence.

## Where deleted data can remain
| Area | What the format documents say |
|---|---|
| WAL frames | A WAL is a header plus frames; each frame holds the revised content of one page. A frame is valid only if its salt values match the WAL header and its checksum matches. The WAL file is reused after a checkpoint, so frames left from earlier cycles fail the salt check but may still be physically present |
| Freelist pages | Unused pages (for example after deletes) go on the freelist and are reused when new pages are needed. Freelist leaf pages carry no information and SQLite avoids reading or writing them |
| Freeblocks | Chained unallocated space inside a b-tree page, with a 4-byte header giving next offset and size; fragments of 1-3 bytes are counted separately. A page may be defragmented later |
| Rollback journal | Before an information-bearing page is modified, its original content is written to the journal (freelist leaf pages are not) |

## Tools
- Manual: hex viewer with the file-format specification (page header, cell pointers,
  freeblock chain, WAL frame header).
- SQLite Deleted Records Parser (mdegrazia) is a script that recovers deleted entries from a
  database and writes a TSV or text report (`-f` input, `-o` output, `-r` text report, `-p`
  to print re-purposed b-tree leaf pages).
- Compare a carved record's layout to the table schema before assigning columns.

## Timestamps
Application timestamp formats differ by app and are not defined by the SQLite documentation.
Always record the raw value and state which conversion you applied and why.

## Verify
Recovered deleted records are labelled as such, with source area (WAL frame N, freelist page
M) and the reason you believe the column mapping is correct.

## Checked
Confirmed against the SQLite file-format document (freelist, freeblocks, rollback journal, WAL
frames and validity) and the WAL document (checkpoint triggers, read-only opening rules), and the
parser's GitHub readme (options). Removed as not stated in those pages: the exact read-only URI
string, `PRAGMA secure_delete` behaviour, named tools other than the parser, and the list of
timestamp epochs.
Method: docs-only read of cited pages, 2026-11-08
