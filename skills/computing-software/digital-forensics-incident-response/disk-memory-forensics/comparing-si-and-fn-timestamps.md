---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.comparing-si-and-fn-timestamps
name: comparing-si-and-fn-timestamps
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [si-fn-comparison, ntfs, timestomping, mft, dfir]
level: advanced
status: docs-checked
description: "Compare $STANDARD_INFORMATION and $FILE_NAME timestamps to spot timestomping, using MFTECmd output and $J/$LogFile corroboration."
sources: ["https://github.com/EricZimmerman/MFTECmd", "https://flatcap.github.io/linux-ntfs/ntfs/attributes/file_name.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Comparing $SI and $FN timestamps

**Goal:** every MFT record has timestamps in `$STANDARD_INFORMATION` (0x10) and in each `$FILE_NAME` (0x30) attribute. Disagreements between them are evidence worth chasing.

## What the sources say
- `$FILE_NAME` holds four timestamps (created, altered, MFT changed, read), the parent directory reference, sizes, flags and the name. All fields except the parent directory are only updated when the file name is changed; until then they go out of date.
- `$STANDARD_INFORMATION` is always kept up to date. A file with several names (hard links) has several `$FILE_NAME` attributes, each with its own details and parent.
- So a long-lived file whose `$FN` times differ from `$SI` is normal. What matters is whether the difference is explained by a rename or move, not that one exists.

## Timestomp indicators (judgement, confirm with a second source)
- `$SI` created earlier than `$FN` created, with no rename or move that explains it.
- `$SI` times with zero sub-second precision where the rest of the volume has fractions.
- `$SI` times earlier than the volume creation, OS install, or the parent folder creation.
- A `$J` (USN journal) record for the file's creation at a time later than `$SI` created.
- `$LogFile` records: MFTECmd decodes updates of `$STANDARD_INFORMATION` timestamps (such as a time stomp) with the previous values from the undo data.

## Tool
```cmd
MFTECmd.exe -f "$MFT" --csv "out" --csvf mft.csv
MFTECmd.exe -f "$MFT" --csv "out" --at
MFTECmd.exe -f "$LogFile" -m "$MFT" --csv "out"
MFTECmd.exe -f "$J" -m "$MFT" --csv "out"
```
- By default the `$MFT` output includes `0x30` timestamps only when they differ from `0x10`; `--at` includes all of them.
- `-m` supplies the `$MFT` so `$J` and `$LogFile` paths resolve; for `$J`, paths are as they were when each record was written. Use the `$MFT` and `$J` of the same volume, collected together.
- `$LogFile` output has one row per log record ordered by LSN, with RedoOperation, UndoOperation and Details.
- The `$MFT` CSV ends with a ParseErrors column listing skipped damaged parts of a record.

## Gotchas
- Legitimate software can set `$SI` times (for example extractors preserving archive times), so files from archives can look stomped. Treat indicators as leads.
- A tool that rewrites `$FN` as well defeats a simple `$SI`/`$FN` comparison; rely on `$J` and `$LogFile` corroboration.

## Verify
Each timestomping claim cites the `$SI` and `$FN` values and at least one independent source (`$J`, `$LogFile`, Prefetch, event logs).

## Checked
Date: 2026-11-08.
Read in full: MFTECmd GitHub README; NTFS Documentation (flatcap) "$FILE_NAME (0x30)".
Confirmed: `$FN` layout and four times, update-only-on-rename note, `$SI` always current, hard links, MFTECmd option meanings (`-f`, `-m`, `--csv`, `--csvf`, `--at`), `$J` parent paths at write time, `$LogFile` decoding of `$SI` time-stomp updates with previous values, ParseErrors column.
Removed: the "what updates what" operation table (create/modify/copy/rename behaviour), `NtfsDisableLastAccessUpdate` remark, USN reason names (`FILE_CREATE`, `BASIC_INFO_CHANGE`), MFTECmd column names `Created0x10`, `SI<FN`, `uSecZeros`, `Copied`, and the SANS poster source (login required, no timestamp rules readable). The indicators list is practitioner judgement, kept as leads rather than documented facts.
Method: documentation only; no commands were run.
