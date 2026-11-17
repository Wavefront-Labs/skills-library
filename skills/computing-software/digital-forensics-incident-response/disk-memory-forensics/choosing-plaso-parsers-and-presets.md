---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.choosing-plaso-parsers-and-presets
name: choosing-plaso-parsers-and-presets
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [plaso-parsers, plaso, log2timeline, super-timeline, dfir]
level: advanced
status: docs-checked
description: "Select Plaso parsers and presets (win7, linux, macos, webhist), list and exclude parsers and plugins with log2timeline --parsers, and know how presets are chosen automatically."
sources: ["https://plaso.readthedocs.io/en/latest/sources/user/Parsers-and-plugins.html", "https://plaso.readthedocs.io/en/latest/sources/user/Using-log2timeline.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing Plaso parsers and presets

**Goal:** control which parsers and plugins `log2timeline.py` runs so the timeline contains the right
artefacts, and so you can say which parser produced a row.

## Discover
```bash
log2timeline.py --parsers list          # available parsers, parser plugins and presets
log2timeline.py --info                  # information about supported plugins, parsers, output modules
```
A parser extracts events from one data format (for example `winevtx`); parsers such as `sqlite`, `winreg`
and `text` use plugins for the format variants. A preset is a named list of parsers and plugins.

## How log2timeline picks parsers
1. If `--parsers` is set, its expression is used.
2. Otherwise, if pre-processing found the operating system, every preset that matches that OS is used
   (for example `win7` for Windows NT).
3. Otherwise all parsers and plugins are used.

## Presets (examples, from presets.yaml as listed in the docs)
| Preset | Covers |
|---|---|
| `win7` | `winevtx`, `recycle_bin`, `custom_destinations`, `olecf/olecf_automatic_destinations`, `esedb/file_history`, `esedb/user_access_logging`, `winpca_db0`, `winpca_dic`, `text/powershell_transcript`, plus `win_gen` |
| `win_gen` | `winreg`, `prefetch`, `lnk`, `filestat`, `usnjrnl`, `winjob`, `olecf`, `pe`, `text/setupapi`, `text/winfirewall`, `webhist` and others |
| `win7_slow` | `esedb`, `mft` and `win7` |
| `linux` | `systemd_journal`, `utmp`, `filestat`, `text/syslog`, `text/selinux`, `text/bash_history`, `text/dpkg`, `text/apt_history`, Docker `jsonl` plugins, `webhist` and others |
| `macos` | `asl_log`, `fseventsd`, `plist`, `bsm_log`, `spotlight_storedb`, `mac_keychain`, `utmpx`, several `sqlite` plugins and others |
| `webhist` | `chrome_cache`, `firefox_cache` (Firefox 31 and earlier), `msiecf`, `esedb/msie_webcache`, Chrome, Firefox and Safari history/cookie plugins and others |
| `android`, `ios`, `mactime`, `winxp`, `atlassian` | Mobile, bodyfile, Windows XP and Atlassian sets |

`firefox_cache2` (Firefox 32 and later) is a separate parser and is not in `webhist`; `esedb/srum` is not in `win7`
(only in the full `esedb` parser of `win7_slow` or by naming it).

## Select and exclude
The `--parsers` option takes comma-separated preset, parser and plugin names, case insensitive.
- Plugin syntax is `parser/plugin`, for example `sqlite/chrome_27_history` or `text/winiis`.
- A parser named without a plugin enables all its plugins.
- A leading `!` excludes an element and exclusions take precedence. A plugin can only be excluded if its
  parser is also included, otherwise log2timeline reports an error.
```bash
log2timeline.py --parsers "linux,!text/bash_history" --storage-file timeline.plaso image.raw
log2timeline.py --parsers "sqlite,!sqlite/chrome_27_history" --storage-file timeline.plaso image.raw
log2timeline.py --parsers "win7,text/syslog" --storage-file timeline.plaso image.raw
```
- `filestat` is the "file system stat information" parser and sits inside `win_gen` and `linux`.

## Presets file
Presets live in `plaso/data/presets.yaml` (a different data directory can be given with `--data`). Keys: `name`,
`description`, `operating_systems`, `parsers`, and optional `deprecated` (using a deprecated preset logs a warning).

## Gotchas
- The preset auto-selected from the detected OS can be overridden with `--parsers`.
- Preset contents change between Plaso releases; record the Plaso version used in the case notes.

## Checked
Date: 2026-11-07.
Read in full: Plaso "Parsers and plugins" (parser list, every plugin table, preset table) and "Using log2timeline.py" (basic usage, VSS/partition options, parsers and presets, `--parsers` rules, presets file, `--info`, `--logfile`, filter files).
Confirmed: `--parsers list`, `--info`, selection order, `--parsers` syntax and the three example commands, `!` exclusion rules, presets.yaml keys and `--data`, the preset contents above, `firefox_cache` vs `firefox_cache2`.
Trimmed: the claim that `esedb/srum` and WebCache are inside `win7`, the `macos` unified-logging (aul) claim, "filestat produces the bulk of events" and the MACB wording, the psort `-o dynamic` field line and parser/data_type claim, the `pinfo --report warnings` and per-parser-count Verify step, and the "silently yields nothing" gotcha (none are on the pages).
Method: documentation only; no commands were run.
