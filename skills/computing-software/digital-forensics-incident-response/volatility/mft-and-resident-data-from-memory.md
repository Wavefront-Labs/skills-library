---
id: computing-software.digital-forensics-incident-response.volatility.mft-and-resident-data-from-memory
name: mft-and-resident-data-from-memory
category: computing-software
field: digital-forensics-incident-response
product: volatility
tags: [mftscan, volatility3, mft-in-memory, resident-data, alternate-data-streams, memory-forensics, ntfs, dfir]
level: advanced
status: docs-checked
description: "Carve MFT records, ADS and resident file content from a memory image with Volatility mftscan when disk evidence is missing or was wiped."
sources: ["https://volatility3.readthedocs.io/en/latest/volatility3.plugins.windows.html", "https://github.com/volatilityfoundation/volatility3/blob/develop/volatility3/framework/plugins/windows/mftscan.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFT and resident file content in memory (mftscan)

**Goal:** recover NTFS metadata, and small files whose content is stored inside the MFT
record, from RAM. Useful when the disk is encrypted, wiped, unavailable, or when an attacker
deleted tools that ran from disk.

## Why it works
NTFS caches MFT records in memory. `mftscan` finds them with a signature scan for
`FILE0`, `FILE*` and `BAAD`. Small files keep their data **resident** in the `$DATA`
attribute inside the record, so the record alone can contain the whole file (scripts,
batch files, configs, ransom notes, small payload stagers).

## Commands
```bash
vol -f mem.raw windows.mftscan.MFTScan > mft.txt        # MFT records: record number, attribute type, created/modified/updated/accessed times, filename
vol -f mem.raw windows.mftscan.ADS > ads.txt            # alternate data streams: ADS filename plus hexdump of content
vol -f mem.raw windows.mftscan.ResidentData > res.txt   # records with resident data: filename plus hexdump of content
vol -f mem.raw timeliner.Timeliner                       # MFTScan is a timeliner source, so its timestamps fold into a memory timeline
```
Plugin names and availability vary by Volatility 3 release (the `ADS` and `ResidentData`
classes depend on `MFTScan`); check the installed version with `vol -h`.

## What to look for
- Filenames of attacker tools, scripts and staging archives that no longer exist on disk.
- `$SI` earlier than `$FN` (timestomping), the same check you would run on disk.
- `Zone.Identifier` ADS with `HostUrl`/`ReferrerUrl`: download origin of a file.
- Resident `.bat`/`.ps1`/`.vbs` content: commands run by the attacker.
- Ransom note text resident in records named `README*.txt`.

## Gotchas
- Results are a sample of what happened to be cached, not the full MFT; absence proves nothing.
- Stale records from deleted or older versions coexist; compare record and sequence numbers.
- Records may be partially overwritten; validate fixup arrays before trusting content.

## Self-check
Every recovered filename of interest is placed on the timeline with both `$SI` and `$FN`
times and corroborated against disk or logs where available.

## Checked

- Confirmed: MFTScan, ADS and ResidentData plugin classes, FILE0/FILE*/BAAD signature scan, output columns, MFTScan is a timeliner source.

Method: docs-checked 2026-11-09 against volatility3 develop source plugins/windows/mftscan.py and plugins/timeliner.py. Removed the unconfirmed 1024-byte/700-byte size figures and the manual carving tool names; NTFS timestomping and Zone.Identifier notes are practitioner knowledge not stated in the plugin source.
