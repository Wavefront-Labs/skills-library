---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.parsing-mac-images-with-mac-apt
name: parsing-mac-images-with-mac-apt
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [mac-apt-parsing, macos-forensics, apfs-forensics, plist-forensics, dfir]
level: practitioner
status: docs-checked
description: "Process macOS images and live collections with mac_apt: supported inputs, launch scripts, plugin selection, output folders (Export, mac_apt.db, Log) and validation."
sources: ["https://github.com/ydkhatri/mac_apt", "https://github.com/ydkhatri/mac_apt/wiki", "https://github.com/ydkhatri/mac_apt/wiki/Sample-Usage", "https://github.com/ydkhatri/mac_apt/wiki/Interpreting-Output"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing Mac images with mac_apt

**Goal:** mac_apt (Yogesh Khatri, MIT licence) is a Python framework with plugins that process macOS full disk images or live machines and extract forensic artefacts. The README requires Python 3.10 or above (64-bit).

## Inputs
- README: E01, VMDK, AFF4, DD, split-DD, DMG (no compression), SPARSEIMAGE, UAC collections, Velociraptor collected files and mounted images; native HFS and APFS parsers; encrypted APFS images can be processed with a password or recovery key; sealed system volumes (Big Sur) and separate SYSTEM and DATA volumes (Catalina and later) are supported. `ios_apt` handles iOS and iPadOS images.
- Sample Usage wiki, input types: E01, DD, DMG, VMDK, AFF4 or MOUNTED.

## Launch scripts (Sample Usage)
- `mac_apt.py`: full disk or volume images.
- `mac_apt_artifact_only.py`: individual artefact files (not every plugin is supported).
- `mac_apt_mounted_sys_data.py`: a mounted macOS 10.15+ image with separate SYSTEM and DATA mount points.
- Syntax: `mac_apt.py [-o OUTPUT_PATH] [-x] [-c] [-l LOG_LEVEL] [-p PASSWORD] input_type input_path plugin [plugin ...]`. `-x` adds an Excel report, `-c` adds CSV, `-p` takes a password or Personal Recovery Key, SQLite output is always produced. Write the options before the input type.

```bash
python mac_apt.py -o out -x E01 macbook.E01 WIFI FSEVENTS BASICINFO
python mac_apt.py -o out DD macbook.dd FAST
python mac_apt.py -o ~/output -x MOUNTED / FAST       # live machine
python mac_apt.py -h                                   # lists plugins for your version
```
`FAST` runs most plugins (the wiki lists IDEVICEBACKUPS, SPOTLIGHT and UNIFIEDLOGS as excluded); `ALL` runs all.

## Notable plugins (README list)
`BASICINFO`, `USERS`, `SAFARI`, `CHROMIUM`, `FIREFOX`, `QUARANTINE` (quarantine database and `.LastGKReject`), `FSEVENTS`, `SPOTLIGHT`, `TERMINALSTATE`, `TERMSESSIONS`, `RECENTITEMS`, `NETWORKING`, `WIFI`, `AUTOSTART`, `DOCKITEMS`, `NOTES`, `IMESSAGE`, `SCREENTIME`, `TCC`, `MSOFFICE`, `IDEVICEBACKUPS`, `INSTALLHISTORY`, `XPROTECT`.
- Unified logs: the README marks `UNIFIEDLOGS` as removed because better options exist; `UNIFIEDLOGEXPORT` exports the logs and associated files for external processing. Older wiki pages still show `UNIFIEDLOGS`, so check `-h` on your version.

## Output (Interpreting Output wiki)
- `Export/` holds files copied from the image, with `Export_Files_Log.csv` describing them; names may change to avoid collisions (profile name prefixes).
- `Log.<datetime>.txt` is the console log; `-l` sets its level (default INFO).
- `mac_apt.db` (SQLite, always present) has a table per plugin that found data, plus a disk information table for full disk images; Excel and CSV are optional.

## Validation
- Open the exported source file (plist or SQLite) behind each relied-on finding and confirm values and time conversions.
- Read the log for plugins that failed on the macOS version present.

## Gotchas
- The README warns that the bundled Chainbreaker code (keychain reading) may be flagged as malware by AV or EDR.

## Verify
Plugin outputs relied on in the report are traced to exported source files and confirmed manually.

## Checked
2026-11-08. Confirmed against the mac_apt README, wiki home, Sample Usage and Interpreting Output pages. Corrected: `-x` means Excel (not SQLite export) and `-c` means CSV (not an E01 flag); UNIFIEDLOGS is removed in the current README. Removed as unconfirmed: `extract_apfs_fs.py`, the `uuidtext`/`dsc` collection advice, hours-long FSEvents/Spotlight runtime, and the `Log.txt` file name.
Method: documentation only; no commands were run.
