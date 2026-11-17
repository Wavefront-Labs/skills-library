---
id: computing-software.software-engineering.cobol.gnucobol-files-isam
name: gnucobol-files-isam
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, gnucobol-files-isam, cobol-compiler-gnucobol, gnucobol-bdb, vbisam, file-handler-config]
level: advanced
status: docs-checked
description: "Know which ISAM backend your GnuCOBOL build uses for INDEXED files and how to configure file behavior."
sources:
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
  - https://github.com/OCamlPro/gnucobol
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GnuCOBOL indexed file backends and file handling
**Goal:** portable indexed-file behavior across GnuCOBOL builds.
- Backend is chosen at build time: Berkeley DB (libdb 4.1 or later) is the default; `configure` can instead select CISAM, DISAM or VBISAM, and `--without-db` removes indexed I/O. `cobc -i` shows the build information.
- Runtime tunables live in runtime.cfg: `COB_SYNC` (sync to disk after each write/update, default false), `COB_FILE_PATH`, `COB_SORT_MEMORY` (default 128M; a larger sort goes to disk), `COB_SORT_CHUNK`, and `COB_VARSEQ_FORMAT` for the length prefix of variable-length sequential files.
- LINE SEQUENTIAL behaviour is runtime settings: `COB_LS_FIXED` (fixed-length records instead of stripping trailing spaces), `COB_LS_VALIDATE` (default true, validates data on read with status 09 and write with status 71), `COB_LS_NULLS`, `COB_LS_SPLIT` (default true: a long record is returned as several records with status 06; otherwise truncated with status 04).
- Write a sequential dump for backups and exchange rather than copying index files between builds.

## Gotchas
- Check which backend your package or image was built with before sharing index files.
- Test concurrent access if you need record locking.

## Self-check
Write an indexed file, dump it with a sequential read loop, and rebuild from the dump.

## Checked
2026-11-02. Checked against the GnuCOBOL manual runtime-configuration appendix (config/runtime.cfg) and the README/DEPENDENCIES notes on ISAM handlers in the source. Removed: LMDB, C-ISAM-via-ODBC/OCI handlers (not stated), the claim that files from one backend cannot be read by another and that locking semantics differ by backend, and the claim that defaults changed across releases.

Method: documentation only; no commands were run.
