---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.detecting-secure-deletion-and-wiping-tools
name: detecting-secure-deletion-and-wiping-tools
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [secure-deletion, wiping-tools, sdelete, cipher-w, anti-forensics, dfir]
level: practitioner
status: docs-checked
description: "Detect SDelete and cipher /w use from what the tools do to a volume: 26-rename chains, free-space fill files and execution traces."
sources: ["https://learn.microsoft.com/en-us/sysinternals/downloads/sdelete", "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cipher"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Detecting secure deletion and wiping tools

**Goal:** you usually cannot recover securely wiped content, but you can often show that wiping happened, when, and sometimes what was wiped. That can be the key finding (spoliation, insider cases, attacker clean-up).

## What the tools do (from the vendor pages)
- **SDelete** (Sysinternals, page shows v2.06) overwrites file data and can also clean free space. Options: `-p` passes (default 1), `-s` recurse, `-r` remove read-only, `-q` quiet, `-f` force the argument to be treated as a file, `-c` clean free space, `-z` zero free space.
- To overwrite a deleted file's name it **renames the file 26 times**, replacing each character with a successive alphabetic character; the first rename of `foo.txt` is `AAA.AAA`. It does not overwrite file names left in free directory space, and does not remove names when cleaning free space.
- To clean free space it allocates the largest file it can (non-cached I/O), then the largest cached file, overwrites both, then on NTFS repeatedly fills free MFT records with small files that fit within an MFT record until no new file can be created.
- For compressed, sparse and encrypted files it uses the defragmentation API to find the clusters and overwrites them through raw access.
- **cipher /w:\<directory\>** removes data from available unused disk space on the entire volume (all other parameters ignored); the directory can be anywhere on a local volume, and a mount point affects the volume it points to.

## Artefacts to look for (inference, practice)
These follow from the behaviour above; the pages do not list forensic artefacts.
- A run of rename records for one file with names that progress through the alphabet pattern, ending in deletion, from a file-system change journal or MFT/log parsing. The original name should appear in the first rename record of the chain, so check the earliest record.
- Large temporary files filling a volume, then deleted, around the time of a cipher or SDelete free-space run, and many small files filling MFT slack.
- Execution evidence for the tool (prefetch, Amcache/ShimCache, process creation logs with command lines) if those sources are enabled on the system. Whether SDelete leaves a per-user first-use registry key is not stated on its page; treat any such key as unverified.
- Free space full of zeros or a fixed pattern is consistent with `-z`/`-c` or `cipher /w`, but SSD TRIM, defragmentation and other tools can also zero space; do not attribute it to wiping without execution evidence.

## Workflow (practice)
1. Parse the journal and MFT with your usual tools and filter for the rename chain and the volume-filling temporary files.
2. Correlate with execution artefacts and logon events for the account and time.
3. Check volume shadow copies for pre-wipe copies of the target files.
4. Report the tool, account, time window and any recovered original names.

## Gotchas
- A journal can wrap; old entries may be gone.
- File names left in free directory space survive SDelete per its own page, so they may be recoverable even after a free-space wipe.

## Self-check
You can name the wiping tool, the account and time it ran, and at least one original filename from rename records or shadow copies, or you state that none was recoverable.

## Checked

2026-11-09. Read in full: Microsoft Learn SDelete v2.06 page (options, 26-rename behaviour, free-space method, MFT fill, defragmentation API use, file-name limitation) and the Microsoft Learn cipher page (/w description). Confirmed those behaviours. Removed: the SANS poster source (not readable), prefetch file names, the `HKCU\Software\Sysinternals\SDelete` EULA key, `EFSTMPWP` and `fil*.tmp`, CCleaner and BleachBit and Eraser fingerprints, MFTECmd/PECmd commands and the claim about how the journal records renames or about journal wrap behaviour. The artefact list and workflow are inference or practice, labelled as such.

Method: documentation only; no commands were run.
