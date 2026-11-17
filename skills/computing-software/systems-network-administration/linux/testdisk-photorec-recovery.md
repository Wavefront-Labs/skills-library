---
id: computing-software.systems-network-administration.linux.testdisk-photorec-recovery
name: testdisk-photorec-recovery
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, testdisk, photorec, partition-recovery, file-carving, data-recovery, ddrescue]
level: practitioner
status: docs-checked
description: "Recover lost partitions with testdisk and carve deleted files with photorec: work on an image, analyse and write a partition table, restrict file types and avoid overwriting data."
sources:
  - https://www.cgsecurity.org/wiki/TestDisk_Step_By_Step
  - https://www.cgsecurity.org/wiki/PhotoRec_Step_By_Step
  - https://www.gnu.org/software/ddrescue/manual/ddrescue_manual.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# testdisk and photorec

## 1. Protect the evidence
Stop using the disk. If it is failing, image it first with GNU ddrescue (`ddrescue <infile> <outfile> <mapfile>`; the
mapfile lets you interrupt and resume, and the manual describes a direct disc access option that bypasses the kernel
cache). Run the tools against the image or a copy, and write recovered files to a **different** disk.

## 2. testdisk: partitions and boot sectors
```bash
testdisk /dev/sdb          # or the image; creates testdisk.log
```
Flow from the TestDisk step-by-step guide: create a log, select the disk, choose **Analyse** to check the current
partition structure and look for lost partitions, then **Quick Search**; if a partition is still missing, **Deeper
Search**. Check the listed files to confirm it is the right partition, then use the **Write** menu to save the
partition structure (nothing is written to the MBR until you choose Write), and reboot. For a damaged NTFS boot
sector, **Backup BS** copies the backup boot sector over it.

## 3. photorec: file carving (no filesystem needed)
```bash
photorec /dev/sdb          # or the image
```
PhotoRec works on a whole disk or a partition (including a mapped device such as a decrypted LUKS volume); use
`File Opt` to change which file types are recovered, which reduces false positives. Recovered files are written to
`recup_dir.1`, `recup_dir.2`, ... sub-directories, with original names and paths lost.

## Gotchas
- A wrong partition-table guess written to disk can make things worse: confirm by listing files first.
- Whether deleted data survives on SSDs or encrypted volumes depends on the device and the key: unlock encrypted
  volumes first and run photorec on the mapped device.

## Verify
- [ ] Recovered partition mounts read-only and contents look right before anything is written back.

## Checked
2026-10-28. Confirmed in the TestDisk and PhotoRec step-by-step pages and the GNU ddrescue manual: Analyse, Quick
Search, Deeper Search, Write, reboot, Backup BS, `File Opt`, `recup_dir.N`, whole-disk use, mapped devices, ddrescue
mapfile and direct disc access. Removed as unconfirmed: `ddrescue -d -r3`, partition-table type menu, `p`/`c` file list
keys, `partprobe`, the Free-versus-Whole option wording, exiftool sorting, TRIM claim.
Method: documentation only; no commands were run.
