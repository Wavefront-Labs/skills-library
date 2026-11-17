---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.targeted-plaso-collection-with-filter-files
name: targeted-plaso-collection-with-filter-files
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [plaso-filter-file, super-timeline, plaso, log2timeline, dfir]
level: advanced
status: docs-checked
description: "Speed up Plaso by processing only high-value paths with YAML filter files or Forensic Artifacts names, choose parsers and presets, and know what you exclude."
sources: ["https://plaso.readthedocs.io/en/latest/sources/user/Collection-Filters.html", "https://github.com/ForensicArtifacts/artifacts", "https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Targeted Plaso collection with filter files

**Goal:** by default log2timeline goes through the entire data set. Collection filters (targeted collection) make Plaso collect
events only from files you know are relevant, giving a usable timeline sooner.

## Two methods (cannot be combined)
Plaso supports Forensic Artifacts definitions and filter files; the two collection filters cannot be used simultaneously.

### Forensic Artifacts definitions
Analyst-centric names that resolve to paths, e.g. `WindowsEventLogSystem` refers to `%SystemRoot%\System32\config\SysEvent.evt`.
```
log2timeline.py --artifact-filters WindowsEventLogSystem --storage-file timeline.plaso source.raw
```
- Several names: comma-separated list. Names can instead be stored one per line in a file passed with `--artifact_filters_file`
  (not combinable with `--artifact-filters`).
- Your own definitions (Forensic Artifacts format) can be passed with `--custom-artifact-definitions` and then named in
  `--artifact-filters`.
- The Forensic Artifacts repository is a community-sourced, machine-readable (YAML) knowledge base of forensic artifacts.

### YAML filter files
```
log2timeline.py --file-filter windows.yaml --storage-file timeline.plaso source.raw
```
Attributes of each path filter (documents separated by `---`):
- `description` (optional); `type` (required: `include` or `exclude`); `path_separator` (optional, `/` by default);
  `paths` (one or more absolute paths, each a regular expression).
```yaml
description: Windows Event Log files.
type: include
path_separator: '\'
paths:
- '%SystemRoot%\\System32\\config\\.+[.]evt'
---
description: Exclude Linux binaries.
type: exclude
paths:
- '/usr/bin'
```
Rules from the documentation:
- Inclusion filters are applied before exclusion filters. A directory path includes or excludes its files and subdirectories.
- Path filters are case insensitive regardless of the file system.
- The regular expression is applied per path segment, so it cannot match the separator: `/usr/.+/echo` matches `/usr/bin/echo`
  but not `/usr/local/bin/echo`.
- `%Name%` segments (e.g. `%SystemRoot%`) are replaced by the Windows environment value determined during preprocessing; if the
  result is not absolute the path is ignored and a warning is logged.
- With `\` as separator, escape it in the expression and escape special characters such as `$` (e.g. `'\\[$]BadClus'`).
- Filter files work at source level only: they do not apply to archives or other composite files inside the source.
- An older plain-text filter style also appears in the log2timeline guide (`-f filter`, one path per line, with `{sysregistry}`);
  verify it against your Plaso version.

## Parsers and presets
- Without `--parsers`, preprocessing picks presets matching the detected operating system; if none, all parsers are used.
- `--parsers` takes comma-separated presets, parsers and plugins (case insensitive); `!` excludes and wins over inclusion; a
  plugin is written `parser/plugin` (e.g. `sqlite/chrome_27_history`). Example: `--parsers "win7,text/syslog"`.
- `log2timeline.py --parsers list` and `--info` list what is available.

## Practice
- Keep the filter file with the case; it defines the scope of your timeline.
- Verify what was collected with `pinfo.py --sections sources timeline.plaso`.
- To avoid prompts on multi-partition or VSS images use `--partitions`, `--vss_stores` and `--unattended`.

## Gotchas
Anything not in the filter is invisible: attacker tools in odd paths are missed unless a later full run catches them.

## Checked
Date: 2026-11-08.
Confirmed in the Collection Filters and Using log2timeline pages: everything stated above, including option spellings
(`--artifact-filters`, `--artifact_filters_file`, `--custom-artifact-definitions`, `--file-filter`/`-f`, `--parsers`).
Corrected: the earlier text wrote `--artifact_filters`; the documented spelling is `--artifact-filters`.
Removed (not on the cited pages): the sample Windows path list, shipped `filter_*.yaml` file names, psort command, the claim that
a full run takes a day or a targeted run an hour, and the statement that regex errors silently match nothing.
Method: docs-only read of cited pages, 2026-11-08
