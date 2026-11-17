---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.resident-data-and-mft-slack
name: resident-data-and-mft-slack
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [mft-slack, ntfs, mft, resident-data, dfir]
level: advanced
status: draft
description: "Recover content from resident $DATA attributes and MFT record slack: small files living entirely inside the MFT, remnants of old records, and extraction methods."
sources: ["https://flatcap.github.io/linux-ntfs/ntfs/concepts/file_record.html", "https://github.com/EricZimmerman/MFTECmd", "https://www.sleuthkit.org/sleuthkit/man/icat.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Resident data and MFT slack

**Goal:** NTFS stores small files (under roughly 600-700 bytes in a 1,024-byte record) inside the
MFT record itself. Their content survives deletion until the record is reused, and record slack
can hold remnants of earlier attributes.

## Resident files
- `$DATA` attribute with the non-resident flag = 0; content immediately follows the attribute header.
- Examples: small scripts, batch files, config files, `.lnk` files, small text notes, `Zone.Identifier` ADS.
- Deleted files: the MFT record is marked not-in-use but content remains until reused - a deleted
  ransom note, attacker batch script or LNK can be recovered with full content.

## Extraction
```bash
istat -o <off> image.dd 48213          # shows attributes; resident $DATA content size
icat -o <off> image.dd 48213 > file.bin  # works for resident data too (deleted records included)
MFTECmd.exe -f $MFT --de 48213          # dump a record's details
MFTECmd.exe -f $MFT --dr --csv out\     # --dr dumps resident data files to a folder
```

## MFT record slack
- Space between the end of the used attributes (marked by `0xFFFFFFFF`) and the end of the
  1,024-byte record: may contain parts of earlier, larger attributes (old filenames, old resident data).
- View with a hex viewer from the record's offset (`MFT offset + record_number * 1024`).

## Memory angle
- Volatility `windows.mftscan.MFTScan` and `ResidentData` find MFT records in RAM, including resident content of files already gone from disk.

## Gotchas
- Fixup values (update sequence array) at the end of each 512-byte sector must be applied before reading content that spans the sector boundary; tools do this, manual carving must too.
- Resident data becomes non-resident when it grows; old resident content may remain in slack.

## Verify
Recovered resident content is reported with MFT record number, sequence number and in-use flag state.
