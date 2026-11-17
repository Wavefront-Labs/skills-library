---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.ntfs-mft-and-ads-manual-analysis
name: ntfs-mft-and-ads-manual-analysis
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ntfs, mft, master-file-table, istat, fls, icat, resident-attribute, non-resident-attribute, data-runs, indx, index-slack, alternate-data-stream, ads, timestomping, mtimes, standard-information, filename-attribute, sleuthkit, tsk, dfir]
level: advanced
status: draft
description: "Read NTFS MFT entries by hand with istat/fls/icat: resident vs non-resident attributes, data runs, INDX slack, ADS, and the $SI/$FN timestamp pairs that catch timestomping."
sources: ["https://www.sleuthkit.org/sleuthkit/man/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NTFS MFT and ADS manual analysis

**Goal:** when a plaso/EZ Tools super-timeline (see
computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso)
flags something odd, read the raw MFT entry to confirm it rather than trusting the
parser's interpretation — parsers disagree on edge cases (resident vs non-resident,
corrupted entries, timestomping) and the ground truth is the entry itself.

## 1. Get the entry
```bash
fls -o <offset> image.E01 54321           # resolve an inode/MFT record number to a name
istat -o <offset> image.E01 54321         # dump the raw MFT entry: attributes, times, runs
```
`istat` prints every attribute in the record: `$STANDARD_INFORMATION` (SI), `$FILE_NAME`
(FN), `$DATA`, `$INDEX_ROOT`/`$INDEX_ALLOCATION` for directories, and any `$DATA:name`
alternate streams.

## 2. $SI vs $FN timestamps — the timestomping check
Every file has two independent timestamp sets: `$STANDARD_INFORMATION` (what every tool
and `dir`/`ls` show, user-writable via SetFileTime-style APIs) and `$FILE_NAME` (set at
create/rename, normally untouched by ordinary timestomping tools because writing it
requires a rename, which most malware skips). A real timestomp shows as **SI times
earlier than or equal to FN times in a way inconsistent with normal use** — classically
SI-created == some far-past date while FN-created is the true, recent date. `istat`
prints both blocks; compare them by hand. Note: SI can legitimately predate FN after a
file move/copy that preserves SI but not FN, so corroborate with $LogFile/$UsnJrnl
(computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso
covers extracting those) before calling it anti-forensics.

## 3. Resident vs non-resident data
A file under roughly 700-900 bytes (depends on record/cluster size) stores its `$DATA`
attribute *inside* the MFT record itself (resident) — no cluster runs, the content is
right there in `istat` output. Larger files are non-resident: `istat` prints a run list
(`0 1048576-1048600 (6)` style: VCN range, LCN start, cluster count). `icat` resolves
either case transparently, but when a record is damaged and `icat` fails, read the
run list yourself and pull clusters with `blkcat -o <offset> image.E01 <LCN>`.

## 4. INDX slack and alternate data streams
- A directory's `$INDEX_ALLOCATION` holds 4KB INDX records; when a file is deleted its
  index entry is often left behind as slack inside the still-allocated INDX record
  (the B-tree node shrinks logically but the bytes aren't zeroed). This is a second,
  independent source of deleted-filename evidence beyond the MFT itself — Autopsy's
  "Keyword Search" over raw disk sectors or manual `istat` on the parent directory's
  INDX attribute surfaces it when the MFT record for the deleted file was fully reused.
- **Alternate Data Streams** (`file.txt:hidden`) never show in a normal directory
  listing. `fls -r` lists them (shown as `file.txt:hidden`); `icat` with the full
  `inode-colon-name` extracts one. Check for ADS on any file dropped by malware —
  `Zone.Identifier` (marks a file as downloaded, holds the source URL) is the most
  common legitimate one and is itself useful provenance evidence.

## Verify
- Cross-check any timestomping call against $LogFile/$UsnJrnl, not SI/FN alone.
- For a non-resident file you carved by hand, confirm the recovered size matches the
  attribute's declared real/allocated size in `istat` output.
- List ADS explicitly (`fls -r`) on every file of interest — a default directory
  listing in Explorer, `ls`, and most GUI tools hides them.

Unconfirmed: INDX-slack recovery success rate varies a lot with cluster size and how
much the directory has been reused since deletion — treat any recovered deleted-name
fragment from slack as corroborating, not sole, evidence.
