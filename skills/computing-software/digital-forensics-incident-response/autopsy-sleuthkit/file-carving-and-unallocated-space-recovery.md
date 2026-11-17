---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.file-carving-and-unallocated-space-recovery
name: file-carving-and-unallocated-space-recovery
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [autopsy, sleuthkit, tsk, file-carving, unallocated-space, slack-space, photorec, scalpel, foremost, blkls, blkcat, header-footer-carving, fragmented-files, jpeg-recovery, deleted-file-recovery, data-recovery, dfir]
level: advanced
status: draft
description: "Recover files that have no surviving MFT/inode record by carving unallocated space and slack with blkls, PhotoRec and Scalpel, and judge what carved output is trustworthy."
sources: ["https://www.sleuthkit.org/sleuthkit/man/", "https://www.cgsecurity.org/wiki/PhotoRec"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File carving and unallocated space recovery

**Goal:** recover file content when the normal path — walk the MFT/inode table, find
a record, read its runs — doesn't work, because the record itself is gone (deep
deletion, quick-formatted volume, corrupted $MFT). This is the fallback after
computing-software.digital-forensics-incident-response.autopsy-sleuthkit.disk-image-analysis-and-timeline,
not a replacement for it: always try metadata-based recovery (`fls -rd`, `tsk_recover`)
first, because carved files have no filename, timestamps or path.

## 1. Pull unallocated space out of the image
```bash
mmls image.E01                       # find the partition offset
blkls -o <offset> image.E01 > unalloc.raw   # extracts ONLY unallocated blocks, concatenated
```
`blkls` output is not contiguous with the original disk — block N in `unalloc.raw` is
not at the same offset it was on disk, so any carved "offset" you see is relative to
`unalloc.raw`, not the image. Note this in your report or a reviewer will misread it
as a disk offset. `blkcat` pulls a single known block number instead, useful once
`istat`/`blkstat` on a partially-overwritten MFT entry has told you roughly where a
file's old runs started.

## 2. Carve
```bash
photorec unalloc.raw        # interactive; or /cmd for scripted recovery with a file-type list
scalpel -c scalpel.conf -o out/ unalloc.raw   # header/footer signatures, config enables types per-line
foremost -i unalloc.raw -o out/
```
PhotoRec is the most forgiving for fragmented files (brute-forces plausible continuation
points for JPEG/MOV/ZIP-based formats); Scalpel and foremost are faster and fully
scriptable but recover only contiguous runs between a header and footer match, so a
fragmented file silently truncates or merges with the next file's data. Run more than
one carver when it matters — they disagree, and the disagreement is informative.

## 3. Judge what you got
- **No filename, path, or reliable timestamp.** A carved JPEG proves the bytes existed
  somewhere on the volume; it proves nothing about who put them there or when, unless
  EXIF survived inside the carved data itself.
- **False positives are common.** A header-only match with no real content (e.g. a
  JPEG SOI marker inside unrelated binary data) produces a corrupt or tiny "recovered"
  file. Open and manually review every carved hit before citing it — do not just count
  files.
- **Fragmentation breaks footer-based carvers silently.** A Scalpel/foremost hit that
  opens but looks corrupt partway through is very likely two files' data stitched
  together; cross-check against PhotoRec's attempt at the same offset.
- **Slack space** (the tail of a file's last cluster, between EOF and cluster boundary)
  can hold a *previous* file's remnant data. `blkcat` on the slack-containing block, or
  Autopsy's "File Discovery" slack-space view, surfaces this; it's a separate source
  from unallocated-cluster carving and both should be checked when a specific deleted
  file is being hunted.

## Verify
- Re-run `fls -rd` / `tsk_recover` first and confirm you actually need carving (no
  surviving metadata record) before reporting carved results as the primary recovery.
- Open every carved file and sanity-check header, size and (if applicable) embedded
  metadata before including it in a report; flag any file whose size is suspiciously
  small or that fails to render.
- State in the report that carved files carry no filesystem-provenance (name/path/MTAC
  times) unless those happen to be embedded in the file's own internal metadata.

Unconfirmed: exact Scalpel config tuning for proprietary/less-common container formats —
verify signatures against a known-good sample before trusting a carve of an unusual type.
