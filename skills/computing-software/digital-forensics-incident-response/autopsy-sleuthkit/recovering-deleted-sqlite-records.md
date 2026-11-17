---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.recovering-deleted-sqlite-records
name: recovering-deleted-sqlite-records
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [sqlite-deleted-records, sqlite-forensics, file-carving, deleted-file-recovery, dfir]
level: advanced
status: draft
description: "Recover deleted SQLite rows from freelist pages, freeblocks, unallocated page space and WAL/rollback journals, with tools and validation of results."
sources: ["https://www.sqlite.org/fileformat2.html", "https://www.sqlite.org/wal.html", "https://github.com/mdegrazia/SQLite-Deleted-Records-Parser"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Recovering deleted SQLite records

**Goal:** browsers, chat apps and mobile OSs store evidence in SQLite. Deleted rows often persist
inside the database file or its journals until overwritten or vacuumed.

## Where deleted data hides (SQLite file format)
| Location | What remains |
|---|---|
| **Freeblocks** inside b-tree pages | Deleted cell content minus the first 4 bytes (overwritten by freeblock header) |
| **Unallocated space** within pages (between cell pointer array and cell content) | Older cell remnants |
| **Freelist pages** (whole pages freed) | Entire old pages, intact until reused |
| **WAL file** (`-wal`) | Page versions after the last checkpoint, including pre-delete copies |
| **Rollback journal** (`-journal`) | Original page images for an in-progress transaction |

`PRAGMA secure_delete=ON` (used by some apps) zeroes deleted content; `auto_vacuum` reclaims pages.

## Tools
- Always copy the DB **with** its `-wal` and `-shm`; open copies only (opening triggers checkpoints).
- Parse WAL frames separately before any checkpoint: Walitean, `sqlite_wal` parsers, commercial tools (show each frame's page version).
- Freelist/freeblock carving: `sqlparse.py` (Mari DeGrazia), Belkasoft/AXIOM/Oxygen SQLite recovery, `undark`, `bring2lite`, FQLite.
```bash
python sqlparse_CLI.py -f History -o history_deleted.tsv
```
- Reconstruct rows using the table schema (column count and serial types); varint record headers allow type inference.

## Validation
- Carved records lack integrity guarantees: confirm plausibility (timestamps in range, foreign keys pointing to known rows) and present as "recovered fragment".
- Compare with WAL frame versions to date the deletion (record present in an older frame, absent in a newer one).

## Gotchas
- Opening the live DB in a browser tool commits the WAL into the main file and destroys frame history.
- Truncated first column bytes in freeblocks distort the first field; note it.

## Verify
Each recovered record is reported with its location type (WAL frame N, freelist page P) and validation reasoning.
