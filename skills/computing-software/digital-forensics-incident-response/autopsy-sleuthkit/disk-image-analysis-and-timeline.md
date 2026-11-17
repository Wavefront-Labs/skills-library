---
id: computing-software.digital-forensics-incident-response.autopsy-sleuthkit.disk-image-analysis-and-timeline
name: disk-image-analysis-and-timeline
category: computing-software
field: digital-forensics-incident-response
product: autopsy-sleuthkit
tags: [autopsy, sleuthkit, tsk, the-sleuth-kit, disk-forensics, mmls, fsstat, fls, icat, istat, mactime, tsk_recover, e01, ewf, raw-image, ntfs, mft, deleted-file-recovery, timeline, bodyfile, hash-lookup, nsrl, keyword-search, dfir]
level: practitioner
status: draft
description: "Examine a disk image with The Sleuth Kit CLI and Autopsy: partitions, file listing, deleted-file recovery, bodyfile and mactime timelines, ingest modules."
sources: ["https://www.sleuthkit.org/sleuthkit/man/", "https://sleuthkit.org/autopsy/docs/user-docs/latest/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Disk image analysis and timelines with Autopsy / The Sleuth Kit

**Goal:** go from a verified disk image to a list of relevant files (including deleted
ones) and a filesystem timeline around the incident window, without modifying evidence.

## 0. Before you start
- Work from an image (E01 or raw/dd), never the original drive; verify its hash against
  the acquisition record (see
  computing-software.digital-forensics-incident-response.evidence-handling.forensic-acquisition-and-chain-of-custody).
  `ewfverify image.E01` checks an E01's embedded hashes.
- TSK reads E01 directly if built with libewf (`img_stat image.E01` tells you).

## 1. Find the partitions
```bash
mmls image.E01
# Slot  Start      End        Length     Description
# 002:  0000002048 0001026047 0001024000 NTFS / exFAT (0x07)
```
`Start` is in **sectors** (usually 512 bytes). Every later TSK command takes `-o <start>`.
GPT disks show an EFI system partition, an MSR and then the data partition — pick the big one.
```bash
fsstat -o 2048 image.E01        # filesystem type, cluster size, volume serial, MFT location
```

## 2. List and pull files
```bash
fls -o 2048 -r -p image.E01 > files.txt      # -r recursive, -p full paths
grep '\*' files.txt                            # entries marked * are deleted
istat -o 2048 image.E01 12345                  # metadata for inode/MFT entry 12345: all timestamps, runs
icat  -o 2048 image.E01 12345 > recovered.bin  # content by inode, works for deleted if not overwritten
tsk_recover -o 2048 image.E01 out/             # bulk-recover unallocated files (-a for allocated too)
```
- On NTFS, `istat` shows both **$STANDARD_INFORMATION** and **$FILE_NAME** timestamps.
  $SI is trivially changeable by tools (timestomping); $FN is updated by the kernel
  only on create/rename/move. $SI earlier than $FN, or $SI with zeroed sub-second
  values, is a classic timestomp indicator.
- A deleted file whose MFT entry has been reused shows the *new* file's data; check
  that the size and type make sense before reporting a recovery.

## 3. Build a filesystem timeline
```bash
fls -o 2048 -r -m C: image.E01 > body.txt                    # bodyfile; -m sets the mount prefix
mactime -b body.txt -d -z UTC 2026-09-01..2026-09-15 > timeline.csv
```
- `-d` = comma-delimited; `-z` sets the display timezone. **Keep everything in UTC**
  and note the system's configured timezone separately (registry
  `SYSTEM\CurrentControlSet\Control\TimeZoneInformation`).
- The `macb` column: m=modified, a=accessed, c=metadata changed (MFT change on NTFS),
  b=born/created. Access times are often disabled or lazily updated on Windows — don't
  hang conclusions on `a` alone.
- For anything beyond the filesystem (event logs, registry, browser history), feed the
  image to plaso instead (see
  computing-software.digital-forensics-incident-response.disk-memory-forensics.super-timeline-with-plaso).

## 4. Autopsy (GUI on top of TSK)
1. New Case → set a case folder on a fast local disk (cases get large; network shares
   are slow and can corrupt the case database).
2. Add Data Source → Disk Image → set the **timezone of the source** correctly.
3. Ingest modules worth enabling on a first pass: Recent Activity, Hash Lookup (load
   NSRL to hide known-good and a known-bad set to flag), File Type Identification,
   Extension Mismatch Detector, Keyword Search (add your IOCs as a list), Embedded File
   Extractor, Email Parser, Interesting Files (rules for `*.ps1` in user dirs, etc.).
4. Let ingest finish before trusting result counts; it runs in the background and the
   tree fills incrementally.
5. Tag findings (Notable Item, etc.) as you go and generate the HTML/Excel report from
   tagged items — tags are your audit trail.

## Gotchas
- Wrong offset → `fls` errors like "Cannot determine file system type". Re-check `mmls`.
- BitLocker/FileVault/LUKS volumes look like garbage until decrypted; you need the
  recovery key and a decrypting layer (e.g. dislocker/libbde) — TSK won't do it for you.
- SSDs with TRIM: deleted blocks are often zeroed quickly; don't promise recovery.

## Verify
- [ ] Image hash matches the acquisition record.
- [ ] Partition offset and filesystem confirmed with `mmls` + `fsstat`.
- [ ] Recovered files hashed; deleted-file claims checked for MFT reuse.
- [ ] Timeline produced in UTC with the source timezone documented.
- [ ] Every reported item is tagged in Autopsy or logged with the exact command used.
