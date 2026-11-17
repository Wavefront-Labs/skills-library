---
id: computing-software.systems-network-administration.navidrome.navidrome-scanning-and-scan-cli
name: navidrome-scanning-and-scan-cli
category: computing-software
field: systems-network-administration
product: navidrome
tags: [navidrome, scan, full-scan, quick-scan, scan-target, watcher, library-scan, ndignore]
level: practitioner
status: docs-checked
description: "Scan a Navidrome library from the CLI: quick versus full scans, targeted folders as libraryID:path, target files, and excluding content with .ndignore gitignore rules."
sources: ["https://www.navidrome.org/docs/usage/admin/cli/scan/", "https://www.navidrome.org/docs/usage/library/exclude-content/", "https://www.navidrome.org/docs/usage/configuration/options/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Navidrome scanning

`navidrome scan` starts a scan; the server watches for changes and runs scheduled scans too (`Scanner.Schedule`, `Scanner.WatcherWait`, `Scanner.ScanOnStartup`).

Flags:
- `-f/--full` checks all folders and ignores modification times. Required after changing `Tags` or other tag configuration; a quick scan will not apply them.
- `-t/--target libraryID:folderPath`, repeatable. The path is relative to the library root: `navidrome scan -t 1:Music/Rock -t 2:Audiobooks`.
- `--target-file ./scan-targets.txt`, one target per line, blank lines skipped. If both are given only the file is used.
- Do not pass `--subprocess`; the server uses it internally.

Find library IDs with `navidrome user list` (libraries column shows `id:path`). Docker: `docker compose run --rm navidrome scan --full`.

Exclude content with `.ndignore`:
- A blank `.ndignore` ignores that folder and subfolders.
- Otherwise it uses `.gitignore` syntax (go-gitignore) and cascades into subdirectories; files can be placed in several folders.

```
# comments start with #
*.flac
/untagged/
/unsorted/
!/thursday/taking-inventory-of-a-frozen-lake/*.flac
```
Brace expansion such as `*.{flac,mp3}` does not work; use one line per pattern. A new or changed `.ndignore` is auto-detected or picked up by a quick scan.

Also see `Scanner.FollowSymlinks` and `Scanner.IgnoreDotFolders` in the options reference.

## Checked

2026-11-04. Confirmed against the Navidrome `scan` CLI page, the Exclude Content page and the Configuration Options page: flags, target format, target file rules, `--subprocess`, `.ndignore` behaviour and limits, scanner options. Removed `PID.*` from the full-scan rule (the PID page says changing PIDs triggers a full rescan by itself).

Method: documentation only; no commands were run.
