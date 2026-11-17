---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.diffing-volume-shadow-copies
name: diffing-volume-shadow-copies
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [vss-diff, volume-shadow-copy, vshadowmount, file-differencing, hash-comparison, ransomware, dfir]
level: practitioner
status: draft
description: "Diff Volume Shadow Copies against each other and the live volume to list files added, changed and deleted between snapshots during an intrusion."
sources: ["https://github.com/libyal/libvshadow", "https://www.sleuthkit.org/sleuthkit/man/fls.html", "https://ericzimmerman.github.io/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Diffing shadow copies to find changed files

**Goal:** answer "what changed on this volume between snapshot A and snapshot B (or now)",
which isolates attacker activity inside a known time window.

## Mount the stores
```bash
vshadowinfo -o $((2048*512)) image.raw            # list stores and creation times
mkdir -p /mnt/vss /mnt/base
vshadowmount -o $((2048*512)) image.raw /mnt/vss  # /mnt/vss/vss1 .. vssN (raw volume files)
mkdir -p /mnt/vss1 /mnt/vss3
mount -o ro,loop,show_sys_files,streams_interface=windows /mnt/vss/vss1 /mnt/vss1
mount -o ro,loop,show_sys_files,streams_interface=windows /mnt/vss/vss3 /mnt/vss3
```
On Windows use Arsenal Image Mounter (mount image with shadow copies) or
`mklink /d \vss1 \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\` on a live box.

## Diff approaches
1. **Hash diff (content):**
   ```bash
   (cd /mnt/vss1 && find . -type f -print0 | xargs -0 sha1sum) | sort -k2 > vss1.txt
   (cd /mnt/vss3 && find . -type f -print0 | xargs -0 sha1sum) | sort -k2 > vss3.txt
   diff vss1.txt vss3.txt | grep '^[<>]'
   ```
   Restrict to user, ProgramData, Windows\Temp and System32 to keep it fast.
2. **Metadata diff (faster):** `fls -r -m / /mnt/vss/vss1 > b1.body` per store, then compare
   inode/size/mtime per path; or MFTECmd on each store's `$MFT` and diff by entry/sequence.
3. **Registry diff:** export the same hive from each store and compare with RegRipper output
   or Registry Explorer's compare; shows Run keys, services and accounts added in the window.
4. **Tooling:** `vss_carver`/`vss_catalog` for deleted stores; some commercial suites (and
   Velociraptor `Windows.Forensics.VSS`-style artifacts) automate diffs.

## Interpreting
- New executables or scripts in ProgramData/Temp/Public between two snapshots bound the
  attacker's drop time to between the snapshot creation times.
- Files present in an older store but absent later = deleted tools or wiped evidence.
- System files changed outside patch windows (compare against `Windows Update` logs) are
  suspicious.

## Gotchas
- Shadow copies are block-level and only record changed blocks; mounting produces a full view,
  but stores can be incomplete if storage was reclaimed.
- Exclude noise (Windows Defender definitions, browser caches, `$Recycle.Bin` churn,
  `SoftwareDistribution`).

## Self-check
Each "added/changed/deleted" file you report has its two snapshot times bracketing the change
and a hash from both sides where applicable.
