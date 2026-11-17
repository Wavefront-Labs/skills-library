---
id: computing-software.systems-network-administration.backup-and-recovery.tape-read-verification
name: tape-read-verification
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [tape-verify, tape, bacula-verify, tapealert, restore-testing, media-health]
level: practitioner
status: draft
description: "Verify tapes can be read back: full-read verify jobs in Bacula and other tools, reading on a different drive, TapeAlert and error counters, and drive diagnostics."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html
  - https://man.archlinux.org/man/sg_logs.8
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tape read verification

**Goal:** proof that data on tape is readable, ideally by a different drive than the one that wrote it.

## Why it matters
LTO drives already do read-after-write checking while writing, so a job "OK" means the writing drive could read it at write time. It does not prove another drive (possibly years later) can read it, or that the tape survived transport and storage.

## Tool-level verify
- **Bacula/Bareos**: Verify job comparing tape contents with the catalog:
```
Job { Name = "verify-weekly"; Type = Verify; Level = VolumeToCatalog; Verify Job = "fs01-backup"; ... }
```
  Also `bls -j -V Vol001 /dev/nst0` to list jobs on a tape, `bextract` to restore without a catalog.
- **NetBackup**: `bpverify`; **Commvault**: media verification; **Veeam**: run a test restore from tape to disk.
- **tar/LTFS**: `tar -tvf /dev/nst0 > /dev/null` reads the whole archive; LTFS read files back and compare checksums.

## Drive and media health
```sh
sg_logs -a /dev/sg3 | less          # error counters, TapeAlert flags
tapeinfo -f /dev/sg3                 # TapeAlert flags: cleaning required, media error
```
Vendor tools: IBM ITDT, HPE Library and Tape Tools (LTT), Quantum xTalk, for drive tests and cartridge memory reads (load count, error history).

## Policy
- Verify a sample every week (e.g. one tape per pool) and every tape going to long-term vault.
- Read on a different drive than the writer at least for the vault copy.
- Retire cartridges with rising soft error counts or near rated load counts.

## Gotchas
- Verify jobs tie up drives for hours; schedule outside backup windows.
- Verifying immediately after writing on the same drive proves little; prefer later, other drive.

## Verify
Verification log per tape stored with the tape inventory; failures trigger media replacement and a re-copy.
