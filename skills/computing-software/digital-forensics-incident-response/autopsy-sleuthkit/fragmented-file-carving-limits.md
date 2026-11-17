---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.fragmented-file-carving-limits
name: fragmented-file-carving-limits
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [fragmented-file-carving, file-carving, photorec, scalpel, bifragment-gap-carving, dfir]
level: advanced
status: draft
description: "Understand fragmented file carving limits: why header-footer carving fails, which tools handle fragmentation, validating partial output and how to report carved results."
sources: ["https://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step", "https://github.com/sleuthkit/scalpel", "https://dfrws.org/presentation/carving-contiguous-and-fragmented-files-with-fast-object-validation/", "https://www.sciencedirect.com/science/article/pii/S1742287607000394"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fragmented file carving limits

Carvers find files in unallocated space by signatures. Classic header-to-footer (or header plus max size) carving assumes the file is contiguous. Research (Garfinkel, DFRWS 2007) found a meaningful share of files on real drives are fragmented, especially large files, Outlook PSTs, and files written to nearly full volumes. Carving those blindly yields corrupted or mixed output.

## How tools behave
- **Scalpel / Foremost**: header to footer or max length; fragmented files come out with foreign data in the middle. Fast, good for small contiguous files.
- **PhotoRec**: uses file-system block size and per-format validation; for some formats (JPEG, others) it tries to detect where data stops being valid and can skip blocks, but it is not a general fragmented-file reassembler.
- **Bifragment gap carving** (Garfinkel): handles files in two fragments by testing gaps with format validation; implemented in research tools, not in most mainstream carvers.
- **Smart carving / validation-driven** approaches exist in commercial tools for specific formats (JPEG restart markers, video containers).

## Improving results
1. Carve only unallocated space (`blkls` output) to avoid recovering live files, but map offsets back to the image (`blkls` offset translation) for reporting.
2. Set block size to the file system cluster size so carvers align to cluster boundaries.
3. Use format-aware validators: JPEG decoders (partial grey areas indicate fragmentation), `zip -T` / `7z t` for OOXML, `sqlite3 PRAGMA integrity_check`, PDF parsers.
4. For key file types, try targeted recovery from file-system metadata first (MFT runlists of deleted entries still list fragment locations; `icat -r`), which handles fragmentation correctly while clusters remain unallocated and not overwritten.
5. Consider page-level recovery for databases (SQLite page carving) rather than whole files.

## Reporting
- Say a file was carved, from which offset range, and that it has no file-system metadata (no name, path or timestamps unless embedded, e.g. EXIF).
- State validation outcome: complete, partially valid, invalid. Do not present a partially valid file's content as complete.
- Contiguity is an assumption; say so when results depend on it.

## Gotchas
- SSDs with TRIM leave little unallocated data to carve; zero results are expected, not a tool failure.
- Embedded thumbnails inside carved JPEGs can show the original image even when the main image is corrupt; report them separately.

## Verify
Each carved file cited in a report has its offset range, validation result and hash, and none is described as complete without passing format validation.
