---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.validating-carved-files
name: validating-carved-files
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [carved-file-validation, file-carving, deleted-file-recovery, forensic-report, dfir]
level: practitioner
status: draft
description: "Validate carved files before relying on them: structure checks, fragmentation signs, hash and NSRL matching, metadata limits, and how to report carved results."
sources: ["https://www.cfreds.nist.gov/", "https://www.cgsecurity.org/wiki/PhotoRec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating carved files

**Goal:** carvers produce false positives, truncated and mis-assembled files. Only validated
results belong in a report.

## Structural validation
- Open with a strict parser in a sandbox: JPEG decoders report truncated/corrupt data; `pdfinfo`/`qpdf --check` for PDFs;
  `zip -T` / `7z t` for ZIP-based formats (DOCX/XLSX); `sqlite3 file "PRAGMA integrity_check"`; `ffprobe` for video.
- Visual check for images: grey/garbled lower halves = fragmentation or overwritten tail.
- Tools like PhotoRec already apply format validation; foremost/scalpel header-footer carving does not.

## Fragmentation signs
- File size equals the carver's maximum size setting (footer never found).
- Content switches mid-file (text from another document, image corruption at a cluster boundary).
- Fragmented carving (bifragment gap carving in PhotoRec for some formats) may still assemble wrongly.

## Hash and known-file checks
- Hash carved files; match against known-bad sets and NSRL/known-good to remove OS/application noise.
- Duplicate content across many carved files (same hash) is typical; deduplicate.

## Metadata limits
- Carved files have **no filesystem metadata**: no name, path, owner or MACB times. Do not imply them.
- Internal metadata (EXIF dates, Office core.xml author/created, PDF info dict) remains and can be reported as embedded metadata, with caution (editable).

## Reporting
- State the carving tool/version and settings, the source (unallocated of partition X, offset Y),
  validation performed, and that original file names/times are unknown.
- Include the offset so the result can be reproduced.

## Gotchas
- Thumbnails embedded inside larger files (EXIF thumbnails, Office previews) are carved as separate images; locate the parent before claiming a standalone file existed.

## Verify
A second examiner can reproduce the carve from the stated offset and settings and gets the same hash.
