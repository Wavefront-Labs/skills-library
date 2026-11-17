---
id: computing-software.digital-forensics-incident-response.evidence-handling.kape-modules-for-parsing-artefacts
name: kape-modules-for-parsing-artefacts
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [kape-modules, kape, eric-zimmerman-tools, triage-processing, artefact-parsing, dfir]
level: practitioner
status: docs-checked
description: "Run KAPE modules (.mkape) against collected artefacts to produce CSV with Eric Zimmerman tools: !EZParser, --module, --mdest, --mef, binaries, syncing and logs."
sources: ["https://ericzimmerman.github.io/KapeDocs/", "https://github.com/EricZimmerman/KapeFiles"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KAPE modules for parsing artefacts

**Goal:** turn raw collected artefacts (registry hives, event logs, prefetch, $MFT) into
analysis-ready CSVs in one repeatable step.

## Concepts
- **Targets (`.tkape`)** collect files; **modules (`.mkape`)** run programs against
  collected (or live) files. A module can run only ONE command, so there is a module per
  executable; compound modules such as `!EZParser` reference other modules and chain them.
- Module executables go in `[KAPE directory]\Modules\bin` (or a folder named after the
  module under `Modules`, which is searched first). KAPE does not download binaries for you;
  `kape.exe --mlist . --mdetail` lists modules whose executable is missing, with the download URL.
- `Get-KAPEUpdate.ps1` updates KAPE itself; `kape.exe --sync` refreshes Targets and Modules
  from the KapeFiles repository (by SHA-1 comparison). The `!!ToolSync` module runs tools
  such as RECmd and EvtxECmd with their sync parameters to refresh maps and batch files.
- KAPE needs Administrator rights.

## Run modules on an existing collection
```powershell
kape.exe --msource \triage\WKS0142\C --mdest \parsed\WKS0142 --module !EZParser --mef csv --gui
# or specific modules (comma-separated, no spaces)
kape.exe --msource \triage\WKS0142\C --mdest \parsed\WKS0142 --module PECmd,MFTECmd,EvtxECmd,RECmd_AllBatchFiles,AmcacheParser,AppCompatCacheParser,LECmd,JLECmd,SBECmd --mef csv
```
- `--mef` picks the export format (CSV, txt, JSON...) and overrides the module default; if the
  format does not exist for a module, the first processor is used.
- `--mdest` is the output root; subfolders are created from each module's `Category`.
- `--gui` keeps the console window open until a key is pressed.
- When Target options are used in the same run, `--msource` can be left empty and `--tdest`
  is used. Example: `--tsource C: --tdest \triage\WKS0142 --target KapeTriage`.
- Variables in a module command line include `%sourceDirectory%`, `%destinationDirectory%`,
  `%sourceFile%` and custom ones passed as `--mvars key:value^key2:value2`.

## Key modules
| Module | What the KapeFiles module does |
|---|---|
| `!EZParser` | Compound: AmcacheParser, AppCompatCacheParser, EvtxECmd, JLECmd, LECmd, MFTECmd, PECmd, RBCmd, RecentFileCacheParser, RECmd_DFIRBatch, SBECmd, SQLECmd, SrumECmd, SumECmd, WxTCmd |
| `MFTECmd` | Compound: $Boot, $MFT, $J, $SDS, $I30 and $LogFile modules; category FileSystem |
| `EvtxECmd` | Processes event log files (CSV, XML or JSON); category EventLogs |
| `RECmd_RECmd_Batch_MC` | RECmd with the `RECmd_Batch_MC.reb` batch file; replays transaction logs (`--nl false`); category Registry |
| `RECmd_AllBatchFiles` | Compound: runs every RECmd_* batch module (DFIRBatch, InstalledSoftware, the ASEP modules, UserActivity, etc.) |
| `PECmd` | Processes prefetch files; category ProgramExecution |
| `SrumECmd` | SRUM parser; category SRUMDatabase |
| `AmcacheParser`, `AppCompatCacheParser`, `LECmd`, `JLECmd`, `SBECmd` | Each is its own module in the EZTools folder of KapeFiles |

Results are grouped into one output folder per module category (for example EventLogs,
FileSystem, ProgramExecution, Registry). Open the CSVs in Timeline Explorer, Excel or similar.

## Gotchas
- Sync Targets, Modules and tool maps/batch files before each case (`--sync`, `!!ToolSync`).
- Running modules directly on a live system or mounted directory is slower than running them
  on a collected set, because many more files and folders must be searched; prefer processing
  collected data on the analysis workstation.
- Do not redirect output with `>` in a module CommandLine; use the `ExportFile` property.
- The SRUM database may need repair before SrumECmd can parse it (see the Srum repository README, cited in the module).
- Mount images with Arsenal Image Mounter (exposes a physical device so VSCs are visible);
  the KAPE docs warn against FTK Imager or Dokan for this.
- Check the console log (in `--mdest`, or the `kape.exe` folder after an error) for errors;
  `--debug` and `--trace` increase its detail.

## Method
Compare each run's console log with the modules requested.

## Verify
The console log shows every requested module ran without error and each expected category
folder contains output; spot-check one parser output against the GUI tool.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the KapeDocs pages (Getting started, Modules, Using KAPE, Log files; read from the KapeDocs GitHub source because the docs site is JavaScript only) and the KapeFiles repository README and module files (!EZParser, MFTECmd, EvtxECmd, RECmd_RECmd_Batch_MC, RECmd_AllBatchFiles, PECmd, SrumECmd).
Removed as not stated by the pages: Get-ZimmermanTools, the Kroll_Batch batch name, a single normalised CSV of all event logs, the FileFolderAccess folder, per-tool output descriptions, a ToolRunner log, and the live-footprint claim.
