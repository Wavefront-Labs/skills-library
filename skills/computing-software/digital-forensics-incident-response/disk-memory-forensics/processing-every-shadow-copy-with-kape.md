---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.processing-every-shadow-copy-with-kape
name: processing-every-shadow-copy-with-kape
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [kape-vss, volume-shadow-copy, kape, triage-collection, dfir]
level: practitioner
status: draft
description: "Collect and parse artefacts from all shadow copies at once using KAPE --vss on live systems or mounted images, with deduplication and output layout."
sources: ["https://ericzimmerman.github.io/KapeDocs/", "https://github.com/EricZimmerman/KapeFiles"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Processing every shadow copy with KAPE

**Goal:** a single KAPE run that collects target files from the live volume *and* every shadow
copy, so you get historical hives, event logs and `$MFT` without manual mounting.

## Collect with VSS
```cmd
kape.exe --tsource C: --tdest <OUT>\tout --target !SANS_Triage --vss --dedupe true
```
- `--vss` makes KAPE enumerate shadow copies of the source volume and collect the same targets from each.
- `--dedupe true` (default) hashes files and skips identical copies, so only changed versions are kept.
- Output layout: live files under `tout\C\...`; VSS copies under `tout\vss<N>\...` with the VSS
  creation time recorded in the console log.

## Against a mounted image
- Mount E01 with Arsenal Image Mounter (with "Mount with VSS support"/write-temporary mode) so
  Windows exposes shadow copies, then run KAPE with `--tsource <mounted letter>: --vss`.

## Parse with modules
```cmd
kape.exe --msource <OUT>\tout --mdest <OUT>\mout --module !EZParser --mef csv
```
Modules process files under each vss folder too; output CSVs include the source path so you can
tell live from VSS rows (e.g. EvtxECmd `SourceFile` column).

## Gotchas
- VSS collection multiplies runtime and output size; restrict targets (e.g. `RegistryHives,EventLogs,FileSystem`) when time-critical.
- On live systems, collection from shadow copies does not create new shadows; it reads existing ones.
- Dedupe relies on hashes: identical event log files across VSS are skipped, which is intended.

## Verify
Console log lists each VSS processed with creation time, and outputs contain `vss<N>` paths.
