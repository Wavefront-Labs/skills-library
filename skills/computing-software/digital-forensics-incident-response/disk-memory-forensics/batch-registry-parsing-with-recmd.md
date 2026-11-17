---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.batch-registry-parsing-with-recmd
name: batch-registry-parsing-with-recmd
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [recmd, windows-registry, registry, registry-explorer, kape-modules, dfir]
level: practitioner
status: docs-checked
description: "Parse registry hives at scale with RECmd batch files and plugins: dirty hive log replay with rla, ad-hoc key/value searches, deleted-key recovery and CSV output."
sources: ["https://ericzimmerman.github.io/", "https://github.com/EricZimmerman/RECmd", "https://github.com/EricZimmerman/RegistryPlugins"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Batch registry parsing with RECmd

**Goal:** extract the same set of forensic keys from every hive in a case (or hundreds of triage packages) into one CSV or JSON file, consistently.

## Run a batch
```cmd
RECmd.exe -d triage --bn BatchExamples\DFIRBatch.reb --csv out
RECmd.exe -f NTUSER.DAT --bn BatchExamples\DFIRBatch.reb --csv out --csvf reg.csv
```
- `-f` takes one hive, `-d` searches a directory recursively for hives; one of them is required.
- `--bn` names the batch file (.reb) listing the keys and values to report. The examples in `BatchExamples` ship with RECmd and are mostly community maintained; `--sync` downloads the latest ones. DFIRBatch.reb is the batch file used by RECmd and KAPE, and the RegistryPlugins project recommends it because it uses most of the registry plugins.
- Batch mode needs `--csv` or `--json` (one of them) and writes one file for all hives: `<timestamp>_RECmd_Batch_<batch file name>_Output.csv` unless `--csvf`/`--jsonf` overrides the name.
- Columns: HivePath, HiveType, Description, Category, KeyPath, ValueName, ValueType, ValueData, ValueData2, ValueData3, Comment, Recursive, Deleted, LastWriteTimestamp, PluginDetailFile.
- Keys a registry plugin knows get a row with `(plugin)` as ValueType; ValueData, ValueData2 and ValueData3 hold the parsed fields, and the plugin's full output goes to a timestamped folder in the output directory, named in PluginDetailFile.

## Dirty hives and transaction logs
- A hive is dirty when its sequence numbers differ, or its header checksum is wrong and it has logs. RECmd replays the `.LOG`, `.LOG1` and `.LOG2` files next to it (any case). Without the logs a dirty hive is an error unless `--nl` is given (`--nl` allows logs to be missing).
- `rla` is the companion tool: it replays logs into dirty hives and saves them to `--out` (`--ca` also copies clean ones) for tools that do not apply logs themselves.
- A hive that is in use is read raw (Windows, administrator), with its logs. `--vss` processes all Volume Shadow Copies on the drive given by `-f` or `-d` and needs Windows; `--dedupe` drops duplicates by SHA-1 (first file found wins).
- Deleted keys and values are recovered by default; `--recover false` turns it off. The Deleted column marks them.

## Ad-hoc searches
```cmd
RECmd.exe -d hives --sk "ScreenConnect"                  :: key names
RECmd.exe -d hives --sv "Temp" --regex                   :: value names, regex
RECmd.exe -d hives --sd "powershell"                     :: value data
RECmd.exe -d hives --sa "string"                         :: keys, values, data and slack
RECmd.exe -d hives --base64 20 --minSize 1000            :: values by size in bytes
```
- `--sk`, `--sv`, `--sd`, `--ss` search key names, value names, value data and value slack; `--sa` searches all; `--regex` treats the string as a regular expression; `--literal` stops `--sd`/`--ss` being read as ASCII/Unicode byte strings.
- `--base64 <n>` finds Base64-encoded values of at least n bytes; `--minSize <n>` finds values of at least n bytes.
- `--kn` dumps a key with subkeys and values; `--vn` limits it to one value; `--saveTo` writes `--vn` data in binary.

## Registry Explorer
The GUI sibling: registry viewer with searching, multi-hive support, plugins, and locked-file handling. Use it to spot-check what the batch run reported.

## Gotchas
- Plugins that fail to load ("error loading plugin") are usually blocked DLLs after extraction with the Windows ZIP tool: run `Unblock-File .\Plugins\*.dll`, or extract with 7-Zip or WinRAR.
- Exit code 1 means the tool failed (bad arguments or batch file, unreadable hive or logs, dirty hive without logs, unwritable output, plugin failure); 0 includes damaged hives that were reported but skipped.
- Running against hives copied without their logs gives an older state; collect the logs with the hives.

## Verify
Spot-check a few output rows in Registry Explorer to confirm values and last-write times match.

## Checked
Date: 2026-11-08.
Read in full: Eric Zimmerman tools home page; RECmd GitHub README (options, output, plugins, batch files, rla, exit codes, what's new); RegistryPlugins README ("How Plugins Affect Output").
Confirmed: option names and meanings quoted above, output file name and column list, plugin row behaviour, dirty-hive and log rules, `--nl`/`--recover`/`--vss`/`--dedupe`/`--sync`, rla options, Unblock-File advice, exit codes, DFIRBatch recommendation.
Removed: the hand-written .reb YAML example and field list (ValueName, IncludeBinary, BinaryConvert), the claim that `--nl false` replays logs, the list of hive types `-d` finds, the named plugins applied automatically, "ShellBags lite", the KAPE `RECmd_AllBatchFiles` module remark, and Registry Explorer's "Associated/Unassociated deleted records" labels (none are on the pages).
Method: documentation only; no commands were run.
