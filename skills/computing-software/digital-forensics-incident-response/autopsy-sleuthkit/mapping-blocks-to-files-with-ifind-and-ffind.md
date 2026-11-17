---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.mapping-blocks-to-files-with-ifind-and-ffind
name: mapping-blocks-to-files-with-ifind-and-ffind
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [ifind, ffind, sleuthkit, blkcat, blkstat, keyword-hit-to-file, inode-mapping, dfir]
level: practitioner
status: docs-checked
description: "Map a keyword hit or disk offset to its data unit, owning inode and filename with TSK blkstat, ifind and ffind, including deleted and unallocated cases."
sources: ["https://www.sleuthkit.org/sleuthkit/man/ifind.html", "https://www.sleuthkit.org/sleuthkit/man/ffind.html", "https://www.sleuthkit.org/sleuthkit/man/blkstat.html", "https://www.sleuthkit.org/sleuthkit/man/blkcalc.html", "https://www.sleuthkit.org/sleuthkit/man/istat.html", "https://www.sleuthkit.org/sleuthkit/man/mmls.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping blocks to files with ifind and ffind

**Goal:** you have a byte offset (from a keyword search, YARA or a hex editor) and need to know which file it belongs to, whether that data unit is allocated, and its metadata. Work on a copy or read-only image.

## Steps
```bash
mmls image.dd      # partition layout in sectors (start sector, length)
```
`-o` on every TSK tool below is the sector offset where the file system starts (e.g. the partition start from `mmls`). The device sector size is 512 bytes unless the image format says otherwise (`-b`).

1. **Convert the offset** to a file system data unit: subtract the partition start in bytes (start sector x sector size), divide by the file system's block or cluster size.
2. **Is the unit allocated?** `blkstat -o <start> image.dd <unit>` shows allocation status.
3. **Which metadata structure owns it?** `ifind -o <start> -d <unit> image.dd` finds the metadata structure that has allocated the data unit; the page notes it can sometimes return an unallocated structure. Add `-a` to find all of them.
4. **What is its name?** `ffind -o <start> image.dd <inode>` (`-a` all names; `-d` deleted entries only, `-u` undeleted only; with some file systems it finds deleted names).
5. **Metadata and content:** `istat -o <start> image.dd <inode>` (times, size, owner, and the disk units allocated), `icat -o <start> image.dd <inode> > out.bin` (`-r` tries recovery for a deleted file).
6. **View the raw unit:** `blkcat -o <start> image.dd <unit>`.

Reverse lookup, name to metadata: `ifind -o <start> -n /path/to/file image.dd`.

## When it returns nothing
- **Unallocated unit, no owner:** the data is in free space; report it as unallocated with offset, and look for deleted metadata entries that still point at it.
- **Slack:** the unit is allocated to a file but the hit lies beyond its size; compare against the size `istat` reports.

## Unallocated-space offsets
If you searched `blkls` output, `blkcalc -o <start> -u <unalloc_unit> image.dd` gives the unit's address in the original image (`-d` goes the other way; `-s` is for the slack image).

## Self-check
Every reported hit states offset, data unit, allocation status, owning file (or "unallocated") and the command chain used.

## Checked
2026-11-01. Confirmed on the Sleuth Kit man pages: ifind (`-d`, `-n`, `-a`, `-o`, `-b` 512 default, unallocated note), ffind (`-a`, `-d`, `-u`, deleted names), blkstat (allocation status, `-o`), blkcalc (`-u`, `-d`, `-s`), istat (fields shown, allocated units), icat (`-r`, `-o`), blkcat (`-o`), mmls (sector units). Removed: sample output formats, "Inode not found" message, asterisk marking deleted names, NTFS resident-data/`$MFT` guidance, `fsstat` block-size extraction, `fls -rd` step (page confirms flags but not these uses).
Method: documentation only; no commands were run.
